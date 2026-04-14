import requests
from bs4 import BeautifulSoup
import os
import csv
import io
import re
from urllib.parse import urljoin

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
        
        # Dictionary to store found links per year
        # Key: Year (int), Value: URL (str)
        year_to_link = {}

        # Scan for all potential resource links
        # Looking into all links and specifically checking titles/text
        for a_tag in soup.find_all('a', href=True):
            href = a_tag.get('href', '')
            # Combine title and text to find year info
            label = (a_tag.get('title', '') + " " + a_tag.get_text()).strip()
            
            # Filter for CSV resources within our year range
            if 'csv' in href.lower() or 'csv' in label.lower():
                # Extract 3-digit ROC year (e.g., 106, 114)
                match = re.search(r'(\d{3})', label)
                if match:
                    roc_year = int(match.group(1))
                    if START_YEAR_ROC <= roc_year <= END_YEAR_ROC:
                        # Fix relative URLs
                        full_url = urljoin(DATASET_URL, href)
                        year_to_link[roc_year] = full_url

        if not year_to_link:
            print("No matching CSV resources found. The website structure might have changed.")
            return

        sorted_years = sorted(year_to_link.keys())
        print(f"Discovered resources for ROC years: {sorted_years}")

        merged_data = []
        header = None

        for year in sorted_years:
            link = year_to_link[year]
            print(f"Downloading year {year} from: {link}")
            
            try:
                file_res = requests.get(link, headers=headers, timeout=30)
                file_res.raise_for_status()
                
                # Handle potential encoding issues (UTF-8 with BOM is common in Taiwan Gov Data)
                content = file_res.content.decode('utf-8-sig')
                
                f = io.StringIO(content)
                reader = csv.reader(f)
                rows = list(reader)
                
                if not rows:
                    continue
                
                # Capture header from the first successful file
                if header is None:
                    header = rows[0]
                    merged_data.append(header)
                
                # Add data rows, skip header of subsequent files
                data_rows = rows[1:] if header else rows
                merged_data.extend(data_rows)
                print(f"Added {len(data_rows)} rows from ROC {year}")

            except Exception as download_error:
                print(f"Failed to download year {year}: {download_error}")

        if not merged_data:
            print("No data collected to merge.")
            return

        # Save merged data
        save_path = os.path.join(DATA_DIR, "holiday_data.csv")
        with open(save_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerows(merged_data)
        
        print(f"Success! Total records: {len(merged_data) - 1}. Saved to: {save_path}")

    except Exception as e:
        print(f"Scraper error: {e}")

if __name__ == "__main__":
    scrape_data()