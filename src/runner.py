from src.page import HomePage, MyAccountsPage, SignOnV2Page
from src.parser import AccountPageIdentifier
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
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

    def __init__(self, account, url, logger):
        self.logger = logger
        self.driver =webdriver.Remote(
            command_executor='http://selenium-server:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)
        self.driver.get('https://bankofamerica.com')
        self.account = account
        self.url = 'api:80'

    def quit(self):
        self.driver.close()

    def start(self):

        login_page = HomePage(self.driver)

        self.logger.info('Attempting login for ' + self.account['name'])

        login_page.login(self.account['username'], self.account['password'])

        if self.driver.current_url == "https://secure.bankofamerica.com/login/sign-in/entry/signOnV2.go":

            if not self.account['security_questions']:
                self.logger.error('Security questions not configured, cannot continue.')
                exit(1)

            self.logger.info('Security question detected for ' + self.account['name'] + '. Attempting sign in.')

            sign_on_v2 = SignOnV2Page(self.driver)

            question = sign_on_v2.get_question()

            my_answer = self.account['security_questions'][question]

            if not my_answer:
                self.logger.error('Could not find correct security question answer for account ' + self.account['name'])
                exit(1)

            sign_on_v2.insert_answer(my_answer)

            try:
                sign_on_v2.click_recognize()
            except NoSuchElementException:
                pass

            sign_on_v2.submit()

        self.logger.info('Loading My accounts page for ' + self.account['name'])

        my_account_page = MyAccountsPage(self.driver)

        identifier = AccountPageIdentifier(self.driver)

        self.logger.info('Pulling account overviews for' + self.account['name'])

        summary = my_account_page.get_accounts_summary()

        account_summary_list = []

        row_list = []

        for account in summary:

            url = my_account_page.get_account_url(account)

            parsed_account = my_account_page.parse_account_text(account.text)

            parsed_account['url'] = url

            self.logger.info('Found url for ' + parsed_account['name'])

            account_summary_list.append(parsed_account)

        for account in account_summary_list:

            self.logger.info('Attempting to parse account ' + account['name'])

            parser = identifier.get_parser(account['account_type'])

            if parser:
                parser.parse(account, row_list)

                self.logger.info('Successfully parsed ' + account['name'])

        if self.url:
            self.logger.info('Sending transaction data to api:80/transaction')
            r1 = requests.post(self.url + '/transaction', json=row_list)

            self.logger.info(r1)
            self.logger.info('Sending balance data to api:80/update-balance')
            r2 = requests.post(self.url + '/update-balance', json=account_summary_list)
            self.logger.info(r2)
        else:
            self.logger.info('No url set. Printing to stdout')
            print(row_list)
            print(account_summary_list)

        self.quit()
