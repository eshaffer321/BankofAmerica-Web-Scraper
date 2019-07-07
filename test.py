
import requests


data = [[], [], [{'merchant_name': 'SERAO ACADEMY', 'amount': '$99.00', 'category': 'Education: Education', 'date': '07/03/2019', 'description': 'SERAO ACADEMY 408-628-3662 CA', 'transaction_type': 'credit'}]]

r = requests.post('http://localhost:3000/transactions', json=data)