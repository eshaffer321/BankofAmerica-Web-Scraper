import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='boas',
    version='1.1',
    scripts=['boas'],
    author="Erick Shaffer",
    author_email="erick.shaffer321@gmail.com",
    description="Bank of America personal financial web scraper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eshaffer321/BankofAmerica-Web-Scraper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
