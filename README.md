# 🧾 AInvoice – AI-powered Multicurrency Invoice Extractor & Visualizer

AInvoice is a Python-based system that extracts, processes, and analyzes invoices from various formats (PDF, PNG, JPG) using OCR and GPT, converts currencies to euros using real-time FX rates, stores the results in SQLite, and visualizes them in Power BI.

This project is ideal for freelancers, small businesses, and data professionals looking to structure and analyze expense data across different currencies with automation and clarity.

---

## 🚀 Key Features

- 🧠 GPT-based invoice data structuring (OpenAI API)
- 📸 OCR extraction for image-based invoices (Tesseract)
- 💱 Automatic currency conversion to EUR via Fixer.io API
- 🧮 SQLite database generation & SQL querying
- 📊 Interactive Power BI dashboard template
- 🔐 `.env` file for secure API key management

---

## 🛠️ Technologies Used

- Python 3.x
- OpenAI (GPT-4o-mini or similar)
- pytesseract (OCR)
- SQLite3
- Power BI
- Fixer.io (currency exchange rates)
- Pandas, SQLAlchemy, dotenv, PyMuPDF, PIL
- Anaconda + ipykernel for reproducible environments

---

## 📁 Folder Structure

AInvoice/
│
├── main.py
├── functions.py
├── prompt.py
├── queries.sql
├── environment.yml
├── .env                         # Template only – no secrets included
│
├── invoices/                    # Folder with monthly subfolders of invoice files
│   ├── 01_January/
│   ├── 02_February/
│   ├── ...
│   └── 12_December/
│
├── PowerBI/                     # Power BI visual templates
│   ├── Dashboard_AInvoice.pbix             # Power BI clean template
│   ├── Dashboard_AInvoice (reference).pbix # Layout reference
│   └── IMPORTANT - READ.txt                # Dashboard instructions
│
├── data/ (optional)           
│   └── invoices_export.csv      # Optional CSV export from SQLite queries

---

## ⚙️ Prerequisites

1. ✅ [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (Must be installed and path configured)
2. ✅ [SQLite3](https://www.sqlite.org/download.html) CLI or compatible GUI
3. ✅ [Anaconda](https://www.anaconda.com/) (Recommended for environment management)
4. ✅ [Power BI Desktop](https://powerbi.microsoft.com/desktop/)
5. ✅ OpenAI & Fixer.io API keys (free-tier is enough for Fixer.io; OpenAI usage may require budget)

---

## 📦 Installation Guide

# Clone the repository
git clone https://github.com/Isaac5Tayfur/AInvoice.git
cd AInvoice

# Create the environment
conda env create -f environment.yml

# Activate it
conda activate invoice-extractor

# (Recommended) Install ipykernel for notebook compatibility
pip install ipykernel

---

## 🔑 Environment Setup

Open the `.env` file and add your API keys:

OPENAI_API_KEY = "your_openai_key_here"
FIXER_API_KEY = "your_fixer_key_here"

---

## 📂 Where to Place Your Invoices

Place all your invoice files inside:

AInvoice/
└── invoices/
    ├── january/
    │   ├── invoice1.pdf
    │   └── invoice2.jpg
    └── february/
        └── invoice3.png

> Folder names are used only for internal ordering.

---

## ▶️ How to Run the Pipeline

# Inside the activated conda environment
python main.py

This will:
1. Scan all folders in `/invoices`
2. Extract & structure data via OCR and GPT
3. Normalize currencies to EUR
4. Store everything in `invoices.db` (SQLite)

You’ll see console logs showing progress and conversion rates used.

---

## 🧮 Querying the SQLite Database

Launch SQLite via Anaconda Prompt or CMD **in your project path**:

sqlite3 invoices.db

Then run:

.read queries.sql

This script includes:
- Total invoices
- Sum of all imports in EUR
- Grouping by supplier or currency
- CSV export instructions (uncomment in file)

> Tip: To export results, use `.headers on`, `.mode csv`, and `.output invoices_export.csv`

---

## 📊 Power BI Dashboard Usage

1. Open `PowerBI/Dashboard_AInvoice.pbix`
2. Connect to your `invoices.db` via **ODBC** or import `invoices_export.csv`
3. Remap visual elements if necessary

> See `Dashboard_AInvoice (reference).pbix` to understand expected layout and graph structure.

---

## 🌍 Decimal Handling in Power BI

Ensure **regional settings** in Power BI match your CSV format:

- Field: `import` uses **point** as decimal separator
- Set `import` as text format first
- Then, set Power BI regional settings to **English (United States)** or similar

---

## 🛠️ Customization Notes

- You may edit the OpenAI model used in `functions.py` (default: `"gpt-4o-mini"`)
- You can modify the instruction prompt in `prompt.py`
- Add or remove currencies from `currency_map` in `main.py`
- The project supports adding more FX providers if needed

---

## 👨‍💻 Author

Created by [Tayfur Akkaya Clavijo](https://www.linkedin.com/in/tayfur-akkaya-clavijo)  
Hashnode Blog: [Dataverse Diaries](https://tayfur-ac.hashnode.dev)

---

## 📜 License

This project is open-source and free to use under the [MIT License](https://opensource.org/licenses/MIT).