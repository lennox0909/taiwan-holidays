# **Scrape Bot for Taipei Veterans General Hospital HR**

## **Monthly Data Scraping from data.gov.tw**

Since the data pages on [data.gov.tw](https://data.gov.tw/dataset/14718) are not presented as an open API, we need to parse the HTML to find the latest download URL.

## **Directory Structure**

```
.  
├── .github/  
│   └── workflows/  
│       └── scrape.yml      \# GitHub Actions configuration
│       └──static.yml       \# GitHub Actions for static pages deployment
├── data/                   \# Directory for stored data  
│   └── holiday_data.csv    \# Generated API source  
├── scripts/  
│   └── scraper.py          \# Python scraping script  
└── requirements.txt        \# Python dependencies
```

## **Step 1: Prepare requirements.txt**

You need requests for sending HTTP requests and beautifulsoup4 for parsing HTML.

```
requests  
beautifulsoup4
```

## **Step 2: Write the Scraping Script scripts/scraper.py**

This script visits the dataset page, locates the download link, and saves the file.

## **Step 3: Configure GitHub Actions scrape.yml**

Set it to run automatically on the first day of every month.

## **Step 4: Using scraped Data as an API**

Once the workflow runs successfully, `holiday_data.csv` file is hosted on GitHub.
- Access **API** with URL: [holiday_data.csv](https://lennox0909.github.io/taiwan-holidays/data/holiday_data.csv)

