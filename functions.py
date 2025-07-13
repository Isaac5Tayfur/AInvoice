import openai
import fitz  # PyMuPDF
from dotenv import load_dotenv
import os
import pandas as pd
from io import StringIO
from prompt import prompt
from pytesseract import pytesseract
from PIL import Image
import requests

# Load environment variables from the .env file
load_dotenv(".env")

# Get the OpenAI API key from the environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FIXER_API_KEY = os.getenv("FIXER_API_KEY")

# Configure Tesseract OCR path (for Windows only, adjust as needed)
pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(pdf_path):
    """Extracts text from an invoice in PDF format."""
    try:
        doc = fitz.open(pdf_path)  # Open the PDF
        text = "\n".join([page.get_text("text") for page in doc])  # Extract text
        return text
    except Exception as e:
        print(f"❌ Error extracting text from {pdf_path}: {e}")
        return "error"

def extract_text_from_image(image_path):
    """Extracts text from an invoice image (.png, .jpg, .jpeg) using OCR."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"❌ Error extracting text from {image_path}: {e}")
        return "error"

def structure_text(text):
    """Sends the text to OpenAI and retrieves structured CSV response,
    ensuring only valid data is returned or 'error' in case of failure."""
    if text.strip() == "error":
        return "error"

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Replace with the correct model
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in extracting data from invoices. Return only the CSV, without any explanations or extra messages. If you cannot extract data, return exactly the word 'error' without quotes.",
                },
                {
                    "role": "user",
                    "content": prompt + "\n This is the text to parse:\n" + text,
                },
            ],
        )

        csv_response = response.choices[0].message.content.strip()
        return csv_response
    except Exception as e:
        print(f"❌ Error sending text to OpenAI: {e}")
        return "error"

def csv_to_dataframe(csv):
    """Converts CSV text into a pandas DataFrame, ensuring 'import' is numeric."""
    if csv.strip() == "error":
        return pd.DataFrame()  # Return empty DataFrame in case of error

    try:
        # Define data types for each column
        dtype_cols = {
            "invoice_date": str,
            "supplier": str,
            "invoice_description": str,
            "import": str,  # Read as string first to clean commas
            "currency": str,
        }

        # Read CSV into DataFrame with specified data types
        df_temp = pd.read_csv(StringIO(csv), delimiter=";", dtype=dtype_cols)

        # Convert 'import' to float, properly handling comma decimal
        df_temp["import"] = pd.to_numeric(
            df_temp["import"].str.replace(",", "."), errors="coerce"
        )

        return df_temp
    except Exception as e:
        print(f"❌ Error converting CSV to DataFrame: {e}")
        return pd.DataFrame()

def get_exchange_rates(base="EUR", symbols=[]):
    """Get real-time exchange rates from Fixer API for given symbols to base currency (default EUR)."""
    if not FIXER_API_KEY:
        print("❌ FIXER_API_KEY not found in .env")
        return {}

    try:
        symbol_str = ",".join(symbol.upper() for symbol in symbols if symbol != base.lower())
        url = f"https://data.fixer.io/api/latest"
        params = {
            "access_key": FIXER_API_KEY,
            "symbols": symbol_str
        }

        response = requests.get(url, params=params)
        data = response.json()

        if not data.get("success"):
            print(f"❌ Error from Fixer: {data.get('error')}")
            return {}

        # Fixer returns rates with EUR as base on free plan
        return data["rates"]

    except Exception as e:
        print(f"❌ Error fetching exchange rates: {e}")
        return {}
