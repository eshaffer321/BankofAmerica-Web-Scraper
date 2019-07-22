from page import HomePage, MyAccountsPage, SignOnV2Page
from parser import AccountPageIdentifier

from selenium import webdriver
import os
import requests


class Runner:
    """
      Account:
         username: string
         password: string
         name : string
         security_questions: {question: answer, ... ,}
    """

    def __init__(self, account, url):
        self.driver = webdriver.Chrome()
        self.driver.get('https://bankofamerica.com')
        self.account = account
        self.url = url

    def quit(self):
        self.driver.close()

    def start(self):

        login_page = HomePage(self.driver)

        print('Attempting login for ' + self.account['name'])

        login_page.login(self.account['username'], self.account['password'])

        if self.driver.current_url == "https://secure.bankofamerica.com/login/sign-in/entry/signOnV2.go":
            print('Security question detected for ' + self.account['name'] + '. Attempting sign in.')

            sign_on_v2 = SignOnV2Page(self.driver)

            question = sign_on_v2.get_question()

            my_answer = self.account['security_questions'][question]

            sign_on_v2.insert_answer(my_answer)

            sign_on_v2.submit()

        print('Loading My accounts page for ' + self.account['name'])

        my_account_page = MyAccountsPage(self.driver)

        identifier = AccountPageIdentifier(self.driver)

        print('Pulling account overviews ' + self.account['name'])

        summary = my_account_page.get_accounts_summary()

        account_summary_list = []

        row_list = []

        for account in summary:
            url = my_account_page.get_account_url(account)

            parsed_account = my_account_page.parse_account_text(account.text)

            parsed_account['url'] = url

            print('Found url for ' + parsed_account['name'])

            account_summary_list.append(parsed_account)

        for account in account_summary_list:

            print('Attempting to parse account ' + account['name'])

            parser = identifier.get_parser(account['account_type'])

            if parser:
                parser.parse(account, row_list)

            print('Successfully parsed ' + account['name'])

        if self.url:
            print('Sending transaction data to ' + os.getenv('SHEET_API') + '/transaction')
            r1 = requests.post(self.url + '/transaction', json=row_list)
            print(r1)
            print('Sending transaction data to ' + os.getenv('SHEET_API') + '/update-balance')
            r2 = requests.post(self.url + '/update-balance', json=account_summary_list)
            print(r2)
        else:
            print('No url set. Printing')
            print(summary)
            print(account_summary_list)

        self.quit()
