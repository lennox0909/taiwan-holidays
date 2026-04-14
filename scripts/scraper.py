import requests
from bs4 import BeautifulSoup
import os
import csv
import io

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
        
        # Dictionary to store found links per year to avoid duplicates
        # Key: Year (int), Value: URL (str)
        year_to_link = {}

        # Scan for all CSV links
        for a_tag in soup.find_all('a', href=True):
            href = a_tag.get('href', '')
            title = (a_tag.get('title', '') + a_tag.get_text()).strip()
            
            if 'csv' in href.lower() or 'csv' in title.lower():
                # Extract ROC year from title using regex
                match = re.search(r'(\d{3})', title)
                if match:
                    roc_year = int(match.group(1))
                    if START_YEAR_ROC <= roc_year <= END_YEAR_ROC:
                        year_to_link[roc_year] = href

        if not year_to_link:
            print("No matching CSV resources found for the specified ROC years.")
            # Fallback: just try to get the primary one if no year labels found
            return

        print(f"Found resources for years: {sorted(year_to_link.keys())}")

        merged_data = []
        header = None

        # Download and merge each file
        for year in sorted(year_to_link.keys()):
            link = year_to_link[year]
            print(f"Fetching data for year {year}...")
            
            file_res = requests.get(link, headers=headers)
            file_res.encoding = 'utf-8-sig' # Handle BOM
            
            # Use csv module to parse content
            f = io.StringIO(file_res.text)
            reader = csv.reader(f)
            rows = list(reader)
            
            if not rows:
                continue
                
            if header is None:
                header = rows[0]
                merged_data.append(header)
            
            # Append data rows (skipping header of subsequent files)
            merged_data.extend(rows[1:])

        # Save merged data
        save_path = os.path.join(DATA_DIR, "holiday_data.csv")
        with open(save_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerows(merged_data)
        
        print(f"Successfully merged {len(merged_data) - 1} records into: {save_path}")

    except Exception as e:
        print(f"Error during scraping: {e}")

if __name__ == "__main__":
    import re # Ensure re is available inside the function scope if needed or imported globally
    scrape_data()