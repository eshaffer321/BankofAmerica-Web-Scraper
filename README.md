# boa-web-scraper
This web scraper will pull account balances, all transactions from credit and checking accounts. It will then send
this data to another server to be inserted into a google sheet.

# Requirements

This project require a .env file. This will include BOA account credentials as well as the endpoint of the 
data processing server. Additionally, the google sheet api must be enabled, and a service account key must be present.
Here is an example of the .env file
```
GOOGLE_APPLICATION_CREDENTIALS=
SHEET_API=
ERICK_BOA_USERNAME=
ERICK_BOA_PASSWORD=
BRIT_BOA_USERNAME=
BRIT_BOA_PASSWORD=
GCP_BUCKET_NAME=
```

# Data storage
After processing, csvs will be created of the data that is pulled from BOA. If you would like them to be uploaded to 
google cloud storage, uncomment the lines in the main function. 