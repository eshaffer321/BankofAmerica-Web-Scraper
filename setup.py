import setuptools
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='boas',
    version='1.7',
    scripts=['src/boas'],
    author="Erick Shaffer",
    author_email="erick.shaffer321@gmail.com",
    description="Bank of America personal financial web scraper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eshaffer321/BankofAmerica-Web-Scraper",
    keywords=['bankofamerica', 'python', 'boa', 'web scraper', 'selenium',
              'screen scraper', 'data'],
    packages=setuptools.find_packages(),
    install_requires=[
        'knack',
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
