import requests
from bs4 import BeautifulSoup
import os

# Target dataset URL
DATASET_URL = "https://data.gov.tw/dataset/14718"
DATA_DIR = "data"

def scrape_data():
    print(f"Accessing page: {DATASET_URL}")
    
    # Create directory if it doesn't exist
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Simulate browser headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.37 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.37"
    }

    try:
        response = requests.get(DATASET_URL, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for the download link
        # Typically, download links are within <a> tags in the resource section
        # Searching for links containing 'download' or 'resource'
        download_link = None
        for a_tag in soup.find_all('a', href=True):
            href = a_tag.get('href', '').lower()
            if 'download' in href or 'resource' in href:
                download_link = a_tag['href']
                break
        
        if not download_link:
            print("Download link not found. Check if the page structure has changed.")
            return

        print(f"Found download link: {download_link}")

        # Download the file
        file_res = requests.get(download_link, headers=headers)
        file_res.raise_for_status()

        # Save the file as holiday_data.csv
        save_path = os.path.join(DATA_DIR, "holiday_data.csv")
        with open(save_path, 'wb') as f:
            f.write(file_res.content)
        
        print(f"File successfully saved to: {save_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    scrape_data()