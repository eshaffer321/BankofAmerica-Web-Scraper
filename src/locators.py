from selenium.webdriver.common.by import By


class HomePageLocators(object):
    USERNAME_INPUT = (By.ID, 'onlineId1')
    PASSWORD_INPUT = (By.ID, 'passcode1')
    LOGIN_BUTTON = (By.ID, 'signIn')
    ERROR = (By.CLASS_NAME, 'error-message')


class MyAccountLocators(object):
    ACCOUNT_ITEMS = (By.CLASS_NAME, 'AccountItems')
    ACCOUNT_LIST = (By.TAG_NAME, 'li')
    ACCOUNT_URL = (By.CLASS_NAME, 'AccountName')
    ACCOUNT_URL_A_TAG = (By.TAG_NAME, 'a')


''' Credit Locators '''


class CreditLocators(object):
    MAIN_TABLE = (By.CLASS_NAME, 'trans-tbody-wrap')
    ROW_LIST = (By.TAG_NAME, 'tr')


class CreditRowLocators(object):
    DATE_CELL = (By.CLASS_NAME, 'trans-date-cell')

    AMOUNT_CELL = (By.CLASS_NAME, 'trans-amount-cell')

    DESCRIPTION_CELL = (By.CLASS_NAME, 'trans-desc-cell')
    DESCRIPTION_CELL_LINK = (By.TAG_NAME, 'a')

    DETAILS_ARROW = (By.CLASS_NAME, 'expand-trans-from-arrow-ada')

    DETAILS_TABLE = (By.ID, 'BORNEOCARD_NPI_Transaction_Details')
    DETAILS_TABLE_ROW = (By.TAG_NAME, 'tr')


class CreditDetailTable(object):
    MERCHANT_NAME = (By.CLASS_NAME, 'lblMerchantNameVal')
    CATEGORY_NAME = (By.CLASS_NAME, 'lblCategoryName')


''' Checking Locators '''


class CheckingLocators(object):
    TABLE = (By.TAG_NAME, 'tbody')
    TABLE_ROWS = (By.CLASS_NAME, 'record')
    DATE = (By.CLASS_NAME, 'date-action')
    AMOUNT = (By.CLASS_NAME, 'amount')

    TRANSACTION_TYPE = (By.CLASS_NAME, 'type')
    TRANSACTION_DIV = (By.CLASS_NAME, 'ada-hidden')

    DATE_CELL = (By.CLASS_NAME, 'date-action')
    DETAIL_ARROW = (By.TAG_NAME, 'a')


class CheckingDetailsRow(object):
    DETAIL_ROW = (By.CLASS_NAME, 'record-detail')
    DETAIL_CELL = (By.CLASS_NAME, 'transDetailCell')
    DETAIL_CELL_ITEM = (By.TAG_NAME, 'dl')
    CATEGORY = (By.CLASS_NAME, 'lblCategoryName')
    MERCHANT = (By.CLASS_NAME, 'lblMerchantName')
    DESCRIPTION = (By.CLASS_NAME, 'desc-holder')
