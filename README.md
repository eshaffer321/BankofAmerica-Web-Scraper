# BankofAmerica-Web-Scraper


[![PyPI version](https://badge.fury.io/py/boas.svg)](https://badge.fury.io/py/boas)

Selenium web scraper used to pull personal financial data from bankofamerica.com


## About
This web scraper will pull account balances and all transactions from credit and checking accounts. This is meant to be
used with a [node.js server](https://github.com/eshaffer321/BankOfAmerica-2-GoogleSheet-API) which will re-categorize and
insert into a [google sheet](https://docs.google.com/spreadsheets/d/14GYLeWTUBPFWYzXMAJJV4YPmwcsf6vabkQ0-CeHSqHQ/edit#gid=759515713). 

## Installing

To install dependencies, run
```.env
pip install boas
```

## Usage

To run the program in a multi-threaded way, using account details from `accounts.json` run
```.env
boas parse run --threaded-yes --file=accounts.json
```


## Environment variables

This project require a `.env` file or environment variables. The only value required is the sheet api endpoint of the 
[node.js server](https://github.com/eshaffer321/BankOfAmerica-2-GoogleSheet-API).

Here is an example file:
```
SHEET_API=
```

### Account File
The account credentials are stored in a json file. If you would like to login even with the security v2 security,
 you can provide the security answers in the file.
```.env
[{
  "name": "",
  "username": "",
  "password": "",
  "security_questions": {
    "What is the name of your first employer?": "",
    "What is the street you grew up on": "",
    "What is the name of your best friend": ""
  }
}]

```

## How it works

This service first logs in, and then start to collect the account balances and overview from the my accounts page. Next, 
it will visit all checking and credit cards and start collecting the transaction info. This is the following information
that the program collects:

```
merchant_name
category
date
description
amount
```

Only the transactions from the current month are collected. Currently, the savings scraper isn't implemented. For my use
case I did not have many important transactions in savings. The amounts are still collected in the overview and displayed 
in the sheet. If you would like to implement savings, just create another entry in `page.py` and locators in `locator.py`.
To learn more about the page object design pattern, look at [the selenium docs](https://selenium-python.readthedocs.io/page-objects.html)


## Important Notes / Future work

I have not found a way to run selenium in headless mode. It seems bank of america detects this and asks for a capcha, 
which block logging in. I have not explored what options chrome driver might have to mask the headless mode.

## Development
### Testing

There is a few tests located in the test directory. These will test basic login functionality, account summary recording,
and a full functional test of the scraper. Please replace the empty strings with your account information to run these tests.

Here is an example run of a full functional test run:
```.env
python src/FullTests.py
```