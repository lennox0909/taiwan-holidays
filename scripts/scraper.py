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
    print(f"Scraping starts. Target: {DATASET_URL}")
    
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(DATASET_URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Store found links by year
        # key: ROC year (int), value: absolute download URL (str)
        year_to_link = {}

        # Look for resource items in the dataset page
        # data.gov.tw uses structured divs for resources
        # We search for all links that might contain CSV data
        all_links = soup.find_all('a', href=True)
        print(f"Total links found on page: {len(all_links)}")

        for a in all_links:
            href = a['href']
            # Get text from current tag and parent/sibling elements to find context
            context_text = " ".join([
                a.get_text(),
                a.get('title', ''),
                a.get('aria-label', ''),
                a.parent.get_text() if a.parent else ''
            ]).strip()

            # Check if this link refers to a CSV file
            if 'csv' in href.lower() or 'csv' in context_text.lower():
                # Extract 3-digit ROC year (e.g., 106 to 115)
                # Look for patterns like "106年" or "中華民國106"
                match = re.search(r'(\d{3})', context_text)
                if match:
                    roc_year = int(match.group(1))
                    if START_YEAR_ROC <= roc_year <= END_YEAR_ROC:
                        # Fix relative URLs to absolute
                        abs_url = urljoin(DATASET_URL, href)
                        # Avoid duplicates: prioritizing newer URLs if found
                        if roc_year not in year_to_link:
                            year_to_link[roc_year] = abs_url
                            print(f"Target found: ROC {roc_year} -> {abs_url[:60]}...")

        if not year_to_link:
            print("No matching CSV resources found in the range ROC 106-115.")
            return

        sorted_years = sorted(year_to_link.keys())
        print(f"Successfully identified {len(sorted_years)} files: {sorted_years}")

        all_rows = []
        header_set = False

        for year in sorted_years:
            download_url = year_to_link[year]
            print(f"Processing year {year}...")
            
            try:
                # Use a new request to fetch the actual CSV content
                csv_res = requests.get(download_url, headers=headers, timeout=30)
                csv_res.raise_for_status()
                
                # Use 'utf-8-sig' to handle BOM used in Taiwan Gov CSVs
                content = csv_res.content.decode('utf-8-sig')
                
                # Parse CSV
                f = io.StringIO(content)
                reader = csv.reader(f)
                rows = list(reader)
                
                if not rows:
                    continue
                
                # Handle header
                current_header = rows[0]
                data_rows = rows[1:]
                
                if not header_set:
                    all_rows.append(current_header)
                    header_set = True
                
                all_rows.extend(data_rows)
                print(f"Added {len(data_rows)} entries from ROC {year}")

            except Exception as e:
                print(f"Error downloading data for year {year}: {e}")

        if not all_rows:
            print("Merge failed: No data was collected.")
            return

        # Save to file
        output_file = os.path.join(DATA_DIR, "holiday_data.csv")
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerows(all_rows)
        
        print(f"Done! Merged CSV saved to {output_file} with {len(all_rows)-1} records.")

    except Exception as e:
        print(f"Critical error: {e}")

if __name__ == "__main__":
    scrape_data()