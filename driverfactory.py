from selenium import webdriver
import os


class DriverFactory:
    @staticmethod
    def create_driver():
        options = webdriver.ChromeOptions()
        preferences = {"download.default_directory": os.getcwd()}
        options.add_argument('--kiosk')
        options.add_experimental_option("prefs", preferences)
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        return driver
