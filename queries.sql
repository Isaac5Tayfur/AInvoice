-- queries.sql
-- Run with: sqlite3 invoices.db < queries.sql   (CMD)
-- Or: use .read queries.sql inside sqlite3

-- 📋 Show all tables
.tables

-- 🧬 Show schema of the invoices table
.schema invoices

-- 🧾 Preview first 10 invoices
SELECT * FROM invoices LIMIT 10;

-- 🔢 Count total invoices
SELECT COUNT(*) AS total_invoices FROM invoices;

-- 💱 Count invoices per (original) currency
SELECT original_currency, COUNT(*) AS count FROM invoices GROUP BY original_currency;

-- 💰 Total amount per supplier (in euros), sorted from highest to lowest
SELECT supplier, ROUND(SUM(import), 2) AS total_import_eur
FROM invoices
GROUP BY supplier
ORDER BY total_import_eur DESC;

-- 💶 Sum of all invoice amounts (in euros)
SELECT ROUND(SUM(import), 2) AS total_import_eur FROM invoices;

-- ------------------------------------
-- Optional CSV export (uncomment to activate)
-- ------------------------------------
-- .headers on
-- .mode csv
-- .output invoices_export.csv

-- Export selected data (only this will go into the CSV)
-- SELECT * FROM invoices LIMIT 50;

-- Restore console output (only needed if you activated .output command)
-- .output stdout