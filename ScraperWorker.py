import time
import re
import csv
from driverfactory import DriverFactory
from account import Account
from TableParser import ParseFactory


def parse_account_text(text):
    split = text.splitlines()
    balance_regex = '^\$[+-]?[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2}$'
    checking_regex = '(Banking | Checking | Debit | Deposit)'
    savings_regex = 'Savings'
    credit_regex = '(Rewards | Credit | Visa)((?!Savings).)'

    balance = ''
    name = ''
    account_type = ''
    for line in split:
        m1 = re.search(balance_regex, line)
        m2 = re.search(checking_regex, line)
        m3 = re.search(savings_regex, line)
        m4 = re.search(credit_regex, line)
        if m1:
            balance = m1.group(0)
        elif m2:
            name = line
            account_type = 'checking'
        elif m3:
            name = line
            account_type = 'savings'
        elif m4:
            name = line
            account_type = 'credit'

    return {
        'balance': balance,
        'name': name,
        'account_type': account_type
    }


class ScraperWorker:
    def __init__(self, name, username, password):
        self.name = name
        self.driver = DriverFactory.create_driver()
        self.username = username
        self.password = password
        self.account_info_list = []

    def login(self):
        self.driver.get('https://www.bankofamerica.com/')

        self.driver.implicitly_wait(10)

        email = self.driver.find_element_by_id('onlineId1')
        password = self.driver.find_element_by_id('passcode1')
        login_element = self.driver.find_element_by_id('signIn')

        email.send_keys(self.username)
        password.send_keys(self.password)

        login_element.click()

    def initialize_account_info(self):
        account_summary_list = []

        account_dom_element_list = self.driver.find_element_by_class_name("AccountItems").find_elements_by_tag_name(
            "li")

        for account in account_dom_element_list:
            new_account = Account()
            info = parse_account_text(account.text)
            new_account.set_balance(info['balance'])
            new_account.set_name(info['name'])
            new_account.set_account_type(info['account_type'])
            new_account.set_url(account.find_element_by_class_name("AccountName").find_element_by_tag_name(
                'a').get_attribute('href'))
            account_summary_list.append(new_account)

        self.account_info_list = account_summary_list

    def generate_transaction_tables(self):
        for account in self.account_info_list:
            if account.account_type == 'credit' or account.account_type == 'checking':
                parser = ParseFactory.get_parser(account.account_type)
                if parser:
                    account.transaction_table = parser.parse(account, self.driver)
                else:
                    print('Error finding correct parser')
                    self.quit()

    def print_accounts(self):
        for account in self.account_info_list:
            account.print_account_no_transactions()

    def create_csvs(self):
        for account in self.account_info_list:
            if account.account_type == 'checking' or account.account_type == 'credit':

                with open(account.name + account.account_type + str(time.time()) + '.csv', 'w') as csv_file:
                    filewriter = csv.writer(csv_file)
                    filewriter.writerow(['date',
                                         'category',
                                         'amount',
                                         'category',
                                         'description',
                                         'merchant_name'
                                         ])
                    for row in account.transaction_table:
                        filewriter.writerow([row.get_date(),
                                             row.get_category(),
                                             row.get_amount(),
                                             row.get_category(),
                                             row.get_description(),
                                             row.get_merchant_name()
                                             ])

    def quit(self):
        self.driver.quit()
