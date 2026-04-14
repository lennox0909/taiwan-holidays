# **Monthly Data Scraping with GitHub Actions from Data.gov.tw**

Since the data pages on data.gov.tw are often dynamically generated or contain multiple resource links, we need to parse the HTML to find the latest download URL.

## **Recommended Directory Structure**

```
.  
├── .github/  
│   └── workflows/  
│       └── scrape.yml      \# GitHub Actions configuration  
├── data/                   \# Directory for stored data  
│   └── holiday\_data.csv    \# Your generated API source  
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

Set it to run automatically on the first day of every month. Ensure FORCE\_JAVASCRIPT\_ACTIONS\_TO\_NODE24 is set to true to avoid deprecation warnings.

## **Step 4: Using your Data as an API**

Once the workflow runs successfully, your CSV file is hosted on GitHub. You can access it as an API using the following methods:

### **Method A: GitHub Raw URL (Direct Access)**

Every file in a public GitHub repository has a "Raw" URL. This is the simplest way to fetch data.

* **URL Format:** https://raw.githubusercontent.com/{username}/{repo}/main/data/holiday\_data.csv  
* **Usage:** Your application can send a GET request directly to this URL to get the CSV content.

### **Method B: Using a CDN (Better Performance)**

If your application has high traffic, use a CDN like **jsDelivr** to serve the file. It provides better caching and speed.

* **URL Format:** https://cdn.jsdelivr.net/gh/{username}/{repo}@main/data/holiday\_data.csv

### **Method C: GitHub Pages (For static web apps)**

If you enable **GitHub Pages** in your repository settings, the file will be accessible via your custom GitHub Pages domain:

* **URL Format:** https://{username}.github.io/{repo}/data/holiday\_data.csv

## **How to Get Started?**

1. Create a new Private or Public Repository on GitHub.  
2. Upload the provided files to their respective paths.  
3. In the Repository **Settings \> Actions \> General**, ensure **Workflow permissions** is set to Read and write permissions so that the Action has permission to push data back to the Repo.  
4. If your repository is **Private**, you will need to use a **Personal Access Token (PAT)** or GitHub Apps to access the Raw URL from external applications. For **Public** repositories, no authentication is required.