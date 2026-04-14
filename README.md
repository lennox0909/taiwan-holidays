# **Monthly Data Scraping with GitHub Actions from data.gov.tw**

Since the data pages on data.gov.tw are often dynamically generated or contain multiple resource links, we need to parse the HTML to find the latest download URL.

## **Recommended Directory Structure**

```
.
├── .github/  
│   └── workflows/  
│       └── scrape.yml      \# GitHub Actions configuration  
├── data/                   \# Directory for stored data  
│   └── holiday\_data.csv    \# Example data file  
├── scripts/  
│   └── scraper.py          \# Python scraping script  
└── requirements.txt        \# Python dependencies
```

## **Step 1: Prepare requirements.txt**

You need requests for sending HTTP requests and beautifulsoup4 for parsing HTML.

requests  
beautifulsoup4

## **Step 2: Write the Scraping Script scripts/scraper.py**

This script visits the dataset page, locates the download link, and saves the file.

## **Step 3: Configure GitHub Actions scrape.yml**

Set it to run automatically on the first day of every month.

## **How to Get Started?**

1. Create a new Private or Public Repository on GitHub.  
2. Upload the provided files to their respective paths.  
3. In the Repository **Settings \> Actions \> General**, ensure **Workflow permissions** is set to Read and write permissions so that the Action has permission to push data back to the Repo.