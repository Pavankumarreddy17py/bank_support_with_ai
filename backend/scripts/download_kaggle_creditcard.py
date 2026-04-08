"""Download the Kaggle Credit Card Fraud dataset to data/kaggle/creditcard.csv

Requires a valid Kaggle API token (place kaggle.json in ~/.kaggle or set KAGGLE_USERNAME/KAGGLE_KEY env vars)

Usage:
    python backend/scripts/download_kaggle_creditcard.py
"""
import os
import zipfile

try:
    from kaggle.api.kaggle_api_extended import KaggleApi
except Exception as e:
    print("Kaggle API not available. Install with: pip install kaggle")
    raise

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'kaggle')
os.makedirs(DATA_DIR, exist_ok=True)

DATASET = 'mlg-ulb/creditcardfraud'
FILENAME = 'creditcard.csv'

api = KaggleApi()
api.authenticate()

print('Downloading', FILENAME, 'from', DATASET)
# This will download the file to DATA_DIR; if Kaggle serves a zip it may download a zip
api.dataset_download_file(DATASET, file_name=FILENAME, path=DATA_DIR, force=True)

# If Kaggle returned a zip named creditcard.csv.zip, unzip it
zip_path = os.path.join(DATA_DIR, FILENAME + '.zip')
csv_path = os.path.join(DATA_DIR, FILENAME)
if os.path.exists(zip_path):
    print('Unzipping', zip_path)
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(DATA_DIR)
    os.remove(zip_path)

if os.path.exists(csv_path):
    print('Downloaded dataset to', csv_path)
else:
    print('Failed to fetch dataset. Check Kaggle credentials (place kaggle.json in ~/.kaggle)')
    raise SystemExit(1)
