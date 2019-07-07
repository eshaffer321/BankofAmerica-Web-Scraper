from google.cloud import storage
from dotenv import load_dotenv
from ScraperWorker import ScraperWorker
import os
import requests
import glob

load_dotenv()


def run(node):
    try:
        node.login()
        node.initialize_account_info()
        node.generate_transaction_tables()
        node.create_csvs()
        send_account_summary(node)
        send_transactions(node)
    finally:
        node.quit()


def upload_blob(file_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(os.getenv("GCP_BUCKET_NAME"))
    blob = bucket.blob(file_name)

    blob.upload_from_filename(file_name)

    print('File {} uploaded to {}.'.format(
        file_name,
        file_name))


def send_transactions(node):
    accounts_list = []
    for account in node.account_info_list:
        accounts_list.append(serialize_account(account))

    print(accounts_list)
    r = requests.post( os.getenv('SHEET_API') + '/transactions', json=accounts_list)


def serialize_account(account):
    my_list = []
    for row in account.transaction_table:
        new_item = {
            'merchant_name': row.get_merchant_name(),
            'amount': row.get_amount(),
            'category': row.get_category(),
            'date': row.get_date(),
            'description': row.get_description(),
            'transaction_type': account.get_account_type()
        }
        my_list.append(new_item)
    return my_list


def send_account_summary(node):
    payload = []
    for account in node.account_info_list:
        temp_account = {'balance': account.balance, 'account_name': account.get_account_type(), 'name': node.name}
        payload.append(temp_account)
    print(payload)
    r = requests.post(os.getenv('SHEET_API') + '/update-balance', json=payload)


if __name__ == '__main__':
    node = ScraperWorker('erick', os.getenv('ERICK_BOA_USERNAME'), os.getenv('ERICK_BOA_PASSWORD'))
    node1 = ScraperWorker('brit', os.getenv('BRIT_BOA_USERNAME'), os.getenv('BRIT_BOA_PASSWORD'))
    run(node)
    run(node1)
    # files = glob.glob('*.csv')
    # for file in files:
    #     upload_blob(file)
