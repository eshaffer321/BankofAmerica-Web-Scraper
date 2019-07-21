import re
from src.locators import HomePageLocators, MyAccountLocators, CheckingLocators, CheckingDetailsRow, CreditLocators, \
    CreditRowLocators, CreditDetailTable, SignOnV2Locator


class BasePage(object):

    def __init__(self, driver):
        driver.implicitly_wait(10)
        self.driver = driver
        self.timeout = 30


class HomePage(BasePage):

    def set_username(self, username):
        element = self.driver.find_element(*HomePageLocators.USERNAME_INPUT)
        element.send_keys(username)

    def set_password(self, password):
        element = self.driver.find_element(*HomePageLocators.PASSWORD_INPUT)
        element.send_keys(password)

    def click_login_button(self):
        element = self.driver.find_element(*HomePageLocators.LOGIN_BUTTON)
        element.click()

    def login(self, username, password):
        self.set_username(username)
        self.set_password(password)
        self.click_login_button()
        return HomePage(self.driver)

    def login_error_displayed(self):
        error_div = self.driver.find_element(*HomePageLocators.ERROR)
        return error_div.is_displayed()


class MyAccountsPage(BasePage):

    def get_accounts_summary(self):
        account_element = self.driver.find_element(*MyAccountLocators.ACCOUNT_ITEMS)
        account_list = account_element.find_elements(*MyAccountLocators.ACCOUNT_LIST)
        return account_list

    def get_account_url(self, account):
        url = account.find_element(*MyAccountLocators.ACCOUNT_URL).find_element(*MyAccountLocators.ACCOUNT_URL_A_TAG)
        return url.get_attribute('href')

    def parse_account_text(self, account):
        split = account.splitlines()
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


class CheckingPage(BasePage):

    def get_transaction_rows(self):
        transaction_rows = self.driver.find_element(*CheckingLocators.TABLE).find_elements(*CheckingLocators.TABLE_ROWS)
        return transaction_rows

    @staticmethod
    def get_date(row):
        return row.find_element(*CheckingLocators.DATE).text.replace(' ', '')

    @staticmethod
    def get_amount(row):
        return row.find_element(*CheckingLocators.AMOUNT).text

    @staticmethod
    def get_transaction_type(row):
        return row.find_element(*CheckingLocators.TRANSACTION_TYPE).find_element(
            *CheckingLocators.TRANSACTION_DIV).get_attribute(
            'innerHTML')

    @staticmethod
    def click_details_button(row):
        row.find_element(*CheckingLocators.DATE_CELL).find_element(*CheckingLocators.DETAIL_ARROW).click()

    def get_details_row(self, index):
        return self.driver.find_element(*CheckingLocators.TABLE).find_elements(*CheckingDetailsRow.DETAIL_ROW)[index]

    @staticmethod
    def get_details_cell(row):
        return row.find_element(*CheckingDetailsRow.DETAIL_CELL).find_element(*CheckingDetailsRow.DETAIL_CELL_ITEM)

    @staticmethod
    def get_category(row):
        return row.find_element(*CheckingDetailsRow.CATEGORY).text

    @staticmethod
    def get_merchant(row):
        return row.find_element(*CheckingDetailsRow.MERCHANT).get_attribute('innerHTML')

    @staticmethod
    def get_description(row):
        return row.find_element(*CheckingDetailsRow.DESCRIPTION).text


class CreditPage(BasePage):

    def get_transaction_rows(self):
        transaction_rows = self.driver.find_element(*CreditLocators.MAIN_TABLE).find_elements(*CreditLocators.ROW_LIST)
        return transaction_rows

    @staticmethod
    def get_date(row):
        return row.find_element(*CreditRowLocators.DATE_CELL).text.replace(' ', '')

    @staticmethod
    def get_amount(row):
        return row.find_element(*CreditRowLocators.AMOUNT_CELL).text

    @staticmethod
    def get_description(row):
        return row.find_element(*CreditRowLocators.DESCRIPTION_CELL).find_element(
            *CreditRowLocators.DESCRIPTION_CELL_LINK).text

    @staticmethod
    def click_details_button(row):
        row.find_element(*CreditRowLocators.DATE_CELL).find_element(*CreditRowLocators.DETAILS_ARROW).click()

    @staticmethod
    def get_details_rows(row):
        return row.find_element(*CreditRowLocators.DESCRIPTION_CELL).find_element(
            *CreditRowLocators.DETAILS_TABLE).find_elements(*CreditRowLocators.DETAILS_TABLE_ROW)

    @staticmethod
    def get_details_table(row):
        return row.find_element(*CreditRowLocators.DESCRIPTION_CELL).find_element(*CreditRowLocators.DETAILS_TABLE)

    @staticmethod
    def get_merchant(row):
        return row.find_element(*CreditDetailTable.MERCHANT_NAME).text

    @staticmethod
    def get_category(row):
        return row.find_element(*CreditDetailTable.CATEGORY_NAME).text


class SavingPage(BasePage):

    def get_transaction_rows(self):
        transaction_rows = self.driver.find_element(*CheckingLocators.TABLE).find_elements(*CheckingLocators.TABLE_ROWS)
        return transaction_rows

    @staticmethod
    def get_date(row):
        return row.find_element(*CheckingLocators.DATE).text

    @staticmethod
    def get_amount(row):
        return row.find_element(*CheckingLocators.DATE).text

    @staticmethod
    def get_transaction_type(row):
        return row.find_element(*CheckingLocators.TRANSACTION_TYPE).find_element(
            *CheckingLocators.TRANSACTION_DIV).get_attribute(
            'innerHTML')

    @staticmethod
    def click_details_button(row):
        row.find_element(*CheckingLocators.DATE_CELL).find_element(*CheckingLocators.DETAIL_ARROW).click()

    def get_details_row(self, index):
        return self.driver.find_element(*CheckingLocators.TABLE).find_elements(*CheckingDetailsRow.DETAIL_ROW)[index]

    @staticmethod
    def get_details_cell(row):
        return row.find_element(*CheckingDetailsRow.DETAIL_CELL).find_element(*CheckingDetailsRow.DETAIL_CELL_ITEM)

    @staticmethod
    def get_category(row):
        return row.find_element(*CheckingDetailsRow.CATEGORY).text

    @staticmethod
    def get_merchant(row):
        return row.find_element(*CheckingDetailsRow.MERCHANT).get_attribute('innerHTML')

    @staticmethod
    def get_description(row):
        return row.find_element(*CheckingDetailsRow.DESCRIPTION).text


class SignOnV2Page(BasePage):

    def get_question(self):
        return self.driver.find_element(*SignOnV2Locator.ANSWER_SECTION).find_element(*SignOnV2Locator.QUESTION).text

    def insert_answer(self, answer):
        return self.driver.find_element(*SignOnV2Locator.INPUT_ANSWER).send_keys(answer)

    def submit(self):
        self.driver.find_element(*SignOnV2Locator.SUBMIT_BUTTON).click()
