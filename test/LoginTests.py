import unittest
from src.page import HomePage
from selenium import webdriver


class LoginTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://bankofamerica.com')

    def tearDown(self):
        self.driver.close()

    def test_login_incorrect_password(self):
        login_page = HomePage(self.driver)
        login_page.login('test@email.com', 'password123')
        assert login_page.login_error_displayed()
