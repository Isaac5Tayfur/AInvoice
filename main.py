import functions
import pandas as pd
import os
from sqlalchemy import create_engine

# Create an empty DataFrame to store all invoices
df = pd.DataFrame()

# Root directory containing invoices
invoices_dir = "./invoices"

# Iterate over all folders inside the "invoices" directory
for folder in sorted(os.listdir(invoices_dir)):
    folder_path = os.path.join(invoices_dir, folder)

    # Check if the folder is empty
    files = os.listdir(folder_path)
    if not files:
        print(f"⚠️ Skipping empty folder: {folder_path}")
        continue  # Skip this folder and continue with the next

    # Iterate over all files inside the folder
    for file in files:
        file_path = os.path.join(folder_path, file)

        print(f"📄 Processing file: {file_path}")

        # Determine file type and extract text accordingly
        if file.lower().endswith(".pdf"):
            raw_text = functions.extract_text_from_pdf(file_path)
        elif file.lower().endswith((".png", ".jpg", ".jpeg")):
            raw_text = functions.extract_text_from_image(file_path)
        else:
            print(f"⚠️ Unsupported format: {file}, skipping.")
            continue  # Skip unsupported file

        # Structure the extracted text
        structured_text = functions.structure_text(raw_text)

        # Convert structured text to DataFrame
        invoice_df = functions.csv_to_dataframe(structured_text)

        # Append invoice DataFrame to the general DataFrame
        df = pd.concat([df, invoice_df], ignore_index=True)

# Check if df is empty before proceeding
if df.empty:
    print("🚨 No invoices found in any folder! Exiting script.")
    exit()  # Stop execution to prevent errors

# Safe currency conversion using real-time rates from Fixer
# This block handles the conversion of amounts from multiple currencies into euros,
# and preserves the original currency for traceability.

if "currency" in df.columns and "import" in df.columns:
    # Rename 'currency' to 'original_currency' to retain the original input currency
    df.rename(columns={"currency": "original_currency"}, inplace=True)

    # Normalize the original currency strings (lowercase + stripped)
    df["original_currency"] = df["original_currency"].str.lower().str.strip()

    # Define mapping from descriptive currency labels to ISO currency codes (used by Fixer API)
    currency_map = {
        "euros": "EUR",
        "dollars": "USD",
        "pounds": "GBP",
        "yen": "JPY",
        "swiss_francs": "CHF",
        "canadian_dollars": "CAD",
        "australian_dollars": "AUD",
        "yuan": "CNY",
        "swedish_krona": "SEK",
        "norwegian_krone": "NOK",
        "danish_krone": "DKK",
        "rupees": "INR",
        "reais": "BRL",
        "mexican_pesos": "MXN",
        "rands": "ZAR",
        "singapore_dollars": "SGD",
        "hong_kong_dollars": "HKD"
    }

    # Identify which currencies (excluding euros) are present in the data and need conversion
    currencies_to_convert = df["original_currency"].unique()
    target_currencies = [
        currency_map.get(c) for c in currencies_to_convert
        if c != "euros" and currency_map.get(c)
    ]

    # Request current exchange rates from Fixer API (base: EUR, target: listed currencies)
    exchange_rates = functions.get_exchange_rates(base="EUR", symbols=target_currencies)

    # Loop through each currency in the map and apply the conversion if rate is available
    for currency_label, iso_code in currency_map.items():
        if currency_label == "euros":
            continue  # No conversion needed for euros

        if iso_code in exchange_rates:
            rate = exchange_rates[iso_code]
            # Convert all matching rows from this currency to euros
            df.loc[df["original_currency"] == currency_label, "import"] /= rate
            print(f"💱 Converted {currency_label} to euros at 1 {iso_code} = {rate:.4f}")
        else:
            # If exchange rate not found, log and skip this currency
            print(f"⚠️ No exchange rate found for {currency_label} ({iso_code}), skipping.")

else:
    print("⚠️ Column 'currency' or 'import' is missing. Cannot perform conversion.")

# Keep only relevant columns (including original_currency for traceability)
expected_columns = ["invoice_date", "supplier", "invoice_description", "import", "original_currency"]
df = df[[col for col in expected_columns if col in df.columns]]

# Print final shape of DataFrame for debugging
print(f"✅ Processed {df.shape[0]} invoices with {df.shape[1]} columns.")

# Save final DataFrame into a SQLite database
engine = create_engine("sqlite:///invoices.db")

# Save DataFrame to database, appending data instead of replacing
df.to_sql("invoices", engine, if_exists="append", index=False)

# Close database connection
engine.dispose()

print("✅ Process completed. Data saved to 'invoices.db'.")
