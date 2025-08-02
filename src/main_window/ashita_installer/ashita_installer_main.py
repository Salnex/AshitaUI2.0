import os
import requests
import zipfile
from src.config import ASHITA_DOWNLOAD_URL, ASHITA_DOWNLOADS_DIR, PROJECT_ROOT

def download_and_extract_ashita():
    os.makedirs(ASHITA_DOWNLOADS_DIR, exist_ok=True)
    zip_path = os.path.join(ASHITA_DOWNLOADS_DIR, "ashita.zip")
    # Download
    response = requests.get(ASHITA_DOWNLOAD_URL, stream=True)
    response.raise_for_status()
    with open(zip_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    # Extract
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(PROJECT_ROOT)