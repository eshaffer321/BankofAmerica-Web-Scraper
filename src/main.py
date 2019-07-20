from dotenv import load_dotenv
from page import HomePage, MyAccountsPage
from parser import AccountPageIdentifier
from selenium import webdriver
import os
import requests

load_dotenv()


class Runner:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://bankofamerica.com')

    def quit(self):
        self.driver.close()

    def start(self, username, password, name):

        login_page = HomePage(self.driver)

        login_page.login(username, password)

        my_account_page = MyAccountsPage(self.driver)

        identifier = AccountPageIdentifier(self.driver)

        summary = my_account_page.get_accounts_summary()

        account_summary_list = []

        row_list = []

        for account in summary:

            url = my_account_page.get_account_url(account)

            parsed_account = my_account_page.parse_account_text(account.text)

            parsed_account['url'] = url

            account_summary_list.append(parsed_account)

        for account in account_summary_list:

            parser = identifier.get_parser(account['account_type'])

            if parser:

                parser.parse(account, row_list)

        requests.post(os.getenv('SHEET_API') + '/transaction', json=row_list)
        requests.post(os.getenv('SHEET_API') + '/update-balance', json=account_summary_list)


if __name__ == '__main__':
    Runner().start(os.getenv('USER1_BOA_USERNAME'), os.getenv('USER1_BOA_PASSWORD'), 'USER1')
    Runner().start(os.getenv('USER2_BOA_USERNAME'), os.getenv('USER2_BOA_PASSWORD'), 'USER2')
