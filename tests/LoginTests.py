import unittest
from src import HomePage
from selenium import webdriver


class LoginTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://bankofamerica.com')

    def tearDown(self):
        self.driver.close()

    def test_login_incorrect_password(self):
        login_page = HomePage(self.driver)
        login_page.login('tests@email.com', 'password123')
        assert login_page.login_error_displayed()
