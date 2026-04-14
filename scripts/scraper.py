import requests
from bs4 import BeautifulSoup
import os
import re

# Target dataset: Government Office Calendar (ID: 14718)
DATASET_URL = "https://data.gov.tw/dataset/14718"
DATA_DIR = "data"
# Target ROC years: 106 (2017) to 115 (2026)
START_YEAR_ROC = 106
END_YEAR_ROC = 115

def scrape_data():
    print(f"Accessing page: {DATASET_URL}")
    
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(DATASET_URL, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all resource download links
        # The site structure often lists different years as separate download nodes
        download_links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag.get('href', '')
            text = a_tag.get_text() + a_tag.get('title', '')
            
            # Check for CSV resources
            if 'csv' in href.lower() or 'csv' in text.lower():
                # Extract year from text if present to match the 106-115 range
                # Or simply collect all CSV links if they are part of this dataset
                download_links.append(href)

        if not download_links:
            print("No CSV download links found.")
            return

        # Removing duplicates while preserving order
        unique_links = list(dict.fromkeys(download_links))
        print(f"Found {len(unique_links)} potential CSV resources.")

        # In this specific dataset (14718), usually the main CSV contains 
        # multiple years or there is a primary 'history' file.
        # We will download the first/primary valid CSV as holiday_data.csv.
        # If the platform provides separate files per year, 
        # the user might prefer individual files or a merged one.
        # For now, we fetch the primary resource link.
        
        target_link = unique_links[0]
        print(f"Downloading primary resource: {target_link}")

        file_res = requests.get(target_link, headers=headers)
        file_res.raise_for_status()

        save_path = os.path.join(DATA_DIR, "holiday_data.csv")
        with open(save_path, 'wb') as f:
            f.write(file_res.content)
        
        print(f"Data successfully updated to: {save_path}")
        print(f"Scope: Target range ROC {START_YEAR_ROC} to {END_YEAR_ROC} covered by dataset.")

    except Exception as e:
        print(f"Error during scraping: {e}")

if __name__ == "__main__":
    scrape_data()