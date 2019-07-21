from src.page import CheckingPage, CreditPage
from datetime import datetime
import time


class CheckingParser:
    def __init__(self, page):
        self.page = page

    def parse(self, account, row_list):

        index = 0

        self.page.driver.get(account['url'])

        rows = self.page.get_transaction_rows()

        for row in rows:

            new_row = {}

            self.page.driver.execute_script("arguments[0].scrollIntoView();", row)

            date = self.page.get_date(row)

            formatted_date = datetime.strptime(date, '%m/%d/%Y')

            if formatted_date.month != datetime.now().month:
                continue

            transaction_type = self.page.get_transaction_type(row)

            if transaction_type == 'activity type check':

                new_row['merchant_name'] = 'Check'
                new_row['category'] = 'Cash, Checks & Misc: Checks'
                new_row['description'] = transaction_type

            elif transaction_type == 'activity type deposit':

                new_row['merchant_name'] = 'Counter Credit'
                new_row['category'] = 'Income: Deposits'
                new_row['description'] = transaction_type

            else:

                self.page.click_details_button(row)

                time.sleep(1)

                detail_row = self.page.get_details_row(index)

                details_cell = self.page.get_details_cell(detail_row)

                new_row['category'] = self.page.get_category(details_cell)

                new_row['merchant'] = self.page.get_merchant(details_cell)

                new_row['description'] = self.page.get_description(details_cell)

                index = index + 1

            new_row['amount'] = self.page.get_amount(row)

            new_row['date'] = date

            row_list.append(new_row)


class CreditParser:
    def __init__(self, page):
        self.page = page

    def parse(self, account, row_list):

        self.page.driver.get(account['url'])

        rows = self.page.get_transaction_rows()

        for row in rows:

            self.page.driver.execute_script("arguments[0].scrollIntoView();", row)

            date = self.page.get_date(row)

            if date == 'Pending':
                continue

            dt = datetime.strptime(date, '%m/%d/%Y')

            if dt.month != datetime.now().month:
                continue

            amount = self.page.get_amount(row)

            description = self.page.get_description(row)

            self.page.click_details_button(row)

            time.sleep(1)

            merchant_name = self.page.get_merchant(row)

            category = self.page.get_category(row)

            new_row = {
                'amount': amount,
                'description': description,
                'date': date,
                'merchant_name': merchant_name,
                'category': category
            }

            row_list.append(new_row)


class SavingsParser:
    def __init__(self, page):
        self.page = page

    def parse(self, account):
        return 'Not Implemented'


class AccountPageIdentifier:

    def __init__(self, driver):
        self.driver = driver

    def get_parser(self, account_type):

        if account_type == 'checking':
            checking_page = CheckingPage(self.driver)
            return CheckingParser(checking_page)

        elif account_type == 'credit':
            credit_page = CreditPage(self.driver)
            return CreditParser(credit_page)

        else:
            return None
