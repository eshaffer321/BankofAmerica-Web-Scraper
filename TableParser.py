from account import Row
import time
from datetime import datetime


class CreditParse:
    @staticmethod
    def parse(account, driver):
        driver.get(account.url)
        table = driver.find_element_by_class_name('trans-tbody-wrap')
        trans_rows = table.find_elements_by_tag_name("tr")
        row_list = []
        for row in trans_rows:
            driver.execute_script("arguments[0].scrollIntoView();", row)
            new_row = Row()

            # date
            date_cell = row.find_element_by_class_name("trans-date-cell")
            date_text = date_cell.text.replace(' ', '')
            if date_text == 'Pending':
                continue

            dt = datetime.strptime(date_text, '%m/%d/%Y')

            if dt.month != datetime.now().month:
                continue
            new_row.set_date(date_cell.text)

            # amount
            amount = row.find_element_by_class_name("trans-amount-cell")
            new_row.set_amount(amount.text)

            # details td -> a -> span -> text
            description = row.find_element_by_class_name("trans-desc-cell").find_element_by_tag_name('a').text
            new_row.set_description(description)

            # expand details
            arrow_button = date_cell.find_element_by_class_name("expand-trans-from-arrow-ada")
            arrow_button.click()
            time.sleep(1)

            # category
            details_cell = row.find_element_by_class_name("trans-desc-cell")
            details_table = details_cell.find_element_by_id("BORNEOCARD_NPI_Transaction_Details")
            details_rows = details_table.find_elements_by_tag_name("tr")

            data = find_data(details_rows)
            new_row.set_merchant_name(data['merchant_name'])
            new_row.set_category(data['category'])
            row_list.append(new_row)

        return row_list


def find_data(details_row):
    response = {}
    for row in details_row:
        items = row.find_elements_by_tag_name('td')
        if len(items) == 2:
            if items[0].text == 'Merchant Name:':
                response['merchant_name'] = items[1].find_element_by_class_name("lblMerchantNameVal").text
            if items[0].text == 'Transaction Category:':
                response['category'] = items[1].find_element_by_class_name('lblCategoryName').text
    return response


class SavingParse:
    def parse(self):
        print('no')


class CheckingParse:

    @staticmethod
    def parse(account, driver):
        details_index = 0
        driver.get(account.url)
        table = driver.find_element_by_tag_name('tbody')
        trans_rows = table.find_elements_by_class_name("record")
        row_list = []
        for row in trans_rows:

            new_row = Row()

            driver.execute_script("arguments[0].scrollIntoView();", row)

            date = row.find_element_by_class_name('date-action').text

            dt = datetime.strptime(date, '%m/%d/%Y')

            if dt.month != datetime.now().month:
                continue

            amount = row.find_element_by_class_name('amount').text

            trans_type = row.find_element_by_class_name('type').find_element_by_class_name('ada-hidden').get_attribute(
                'innerHTML')

            if trans_type == 'activity type check':
                new_row.set_merchant_name('Check')
                new_row.set_category('Cash, Checks & Misc: Checks')
                new_row.set_description(trans_type)
            elif trans_type == 'activity type deposit':
                new_row.set_merchant_name('Counter Credit')
                new_row.set_category('Income: Deposits')
                new_row.set_description(trans_type)
            else:
                # click the details button
                row.find_element_by_class_name('date-action').find_element_by_tag_name(
                    'a').click()

                time.sleep(1)

                # find next row that was just generated
                details_row = driver.find_element_by_tag_name('tbody').find_elements_by_class_name("record-detail")[
                    details_index]

                detail_cell = details_row.find_element_by_class_name('transDetailCell').find_element_by_tag_name('dl')
                category = detail_cell.find_element_by_class_name('lblCategoryName').text

                merchant = detail_cell.find_element_by_class_name('lblMerchantName').get_attribute('innerHTML')

                description = detail_cell.find_element_by_class_name('desc-holder').text

                new_row.set_category(category)
                new_row.set_merchant_name(merchant)
                new_row.set_description(description)
                details_index = details_index + 1

            new_row.set_date(date)
            new_row.set_amount(amount)
            row_list.append(new_row)

        return row_list


class ParseFactory:
    @staticmethod
    def get_parser(account_type):
        if account_type == 'checking':
            return CheckingParse()
        elif account_type == 'saving':
            return SavingParse()
        elif account_type == 'credit':
            return CreditParse()
        else:
            return None
