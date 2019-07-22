import unittest
from src import HomePage, MyAccountsPage
from src import AccountPageIdentifier
from selenium import webdriver


class FullTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://bankofamerica.com')

    def tearDown(self):
        self.driver.close()

    def test_workflow(self):

        login_page = HomePage(self.driver)

        login_page.login('', '')

        my_account_page = MyAccountsPage(self.driver)

        summary = my_account_page.get_accounts_summary()

        account_summary_list = []

        for account in summary:
            assert account is not None
            url = my_account_page.get_account_url(account)
            assert url is not None
            parsed_account = my_account_page.parse_account_text(account.text)
            assert parsed_account['balance'] is not None
            assert parsed_account['name'] is not None
            assert parsed_account['account_type'] is not None
            parsed_account['url'] = url
            account_summary_list.append(parsed_account)

        identifier = AccountPageIdentifier(self.driver)

        row_list = []

        for account in account_summary_list:

            parser = identifier.get_parser(account['account_type'])

            if parser:
                parser.parse(account, row_list)

        print(row_list)


