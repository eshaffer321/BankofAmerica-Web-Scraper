class Account:
    def __init__(self):
        self.balance = ''
        self.name = ''
        self.account_type = ''
        self.url = ''
        self.transaction_table = []

    def print_account(self):
        print(self.balance)
        print(self.name)
        print(self.account_type)
        print(self.url)
        self.print_table()

    def print_account_no_transactions(self):
        print(self.balance)
        print(self.name)
        print(self.account_type)
        print(self.url)

    def print_table(self):
        for row in self.transaction_table:
            Row.print_given_row(row)

    def set_table(self, table):
        self.transaction_table = table

    def get_table(self):
        return self.transaction_table

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_account_type(self, account_type):
        self.account_type = account_type

    def get_account_type(self):
        return self.account_type

    def set_balance(self, balance):
        self.balance = balance

    def get_name(self):
        return self.balance

    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url


class Row:
    def __init__(self):
        self.date = ''
        self.category = ''
        self.amount = ''
        self.description = ''
        self.merchant_name = ''

    def print_row(self):
        print('Date: ' + self.date)
        print('Category: ' + self.category)
        print('Amount: ' + self.amount)
        print('Description: ' + self.description)
        print('Merchant: ' + self.merchant_name)

    def print_given_row(row):
        print(row.date)
        print(row.category)
        print(row.amount)
        print(row.description)
        print(row.merchant_name)

    def set_date(self, date):
        self.date = date

    def get_date(self):
        return self.date

    def set_category(self, category):
        self.category = category

    def get_category(self):
        return self.category

    def set_amount(self, amount):
        self.amount = amount

    def get_amount(self):
        return self.amount

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description

    def set_merchant_name(self, merchant_name):
        self.merchant_name = merchant_name

    def get_merchant_name(self):
        return self.merchant_name
