# BankofAmerica-Web-Scraper

Selenium web scraper used to pull personal financial data from bankofamerica.com


## About
This web scraper will pull account balances and all transactions from credit and checking accounts. This is meant to be
used with a [node.js server](https://github.com/eshaffer321/BankOfAmerica-2-GoogleSheet-API) which will re-categorize and
insert into a [google sheet](https://docs.google.com/spreadsheets/d/14GYLeWTUBPFWYzXMAJJV4YPmwcsf6vabkQ0-CeHSqHQ/edit#gid=759515713). 

## Installing

Make sure you have pip installed and virtual environment created and active. To install dependencies, run
```.env
pip install
```
## Environment variables

This project require a .env file. This will include BOA account credentials as well as the endpoint of the 
[node.js server](https://github.com/eshaffer321/BankOfAmerica-2-GoogleSheet-API). Multiple user accounts can be placed in
the `.env` file. Please just add the additional runs to `main.py` 

Here is an example file:
```
SHEET_API=
USER1_BOA_USERNAME=
USER1_BOA_PASSWORD=
USER2_BOA_USERNAME=
USER2_BOA_PASSWORD=
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

The first time you run this program, bank of america will ask a security question. I typically try to type it in quickly and
 hit the remember this computer button. This may happen at random intervals while
using the program. There currently isn't a way around these, and I still need to develop a solution. 

Also, I have not found
a way to run selenium in headless mode. It seems bank of america detects this and asks for a capcha, which block loggin in.
 I have not explored what options chrome driver might have to mask the headless mode.
 
## Testing

There is a few tests located in the test directory. These will test basic login functionality, account summary recording,
and a full functional test of the scraper. Please replace the empty strings with your account information to run these tests.

Here is an example run of a full functional test run:
```.env
python FullTests.py
```