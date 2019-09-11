#!/usr/bin/env python

import os
import json
import pygogo as gogo
import logging
import traceback
from flask import Flask
from src.runner import Runner

app = Flask(__name__)

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)

logger = gogo.Gogo(
    'index',
    low_hdlr=gogo.handlers.file_hdlr('var/log/boa-scraper.log'),
    low_formatter=formatter,
    high_level='error',
    high_formatter=formatter).logger


@app.route("/")
def start():
    try:
        path = "var/accounts/" + os.getenv('ACCOUNT_FILE_NAME')

        if os.path.isfile(path):

            logger.info('Found file ' + path)

            with open(path) as json_file:

                data = json.load(json_file)

                if not data[0]['username'] or not data[0]['password']:
                    logger.error('Username and password are required')

                for account in data:
                    runner = Runner(account,
                                    os.getenv('API_URL'),
                                    logger)
                    try:
                        runner.start()
                    except:
                        runner.driver.quit()

        else:
            if not os.getenv('ACCOUNT_FILE_NAME'):

                logger.error('ACCOUNT_FILE_NAME environment variable not set')

            else:

                logger.error('Could not find file: ' + path)

    except Exception as error:
        just_the_string = traceback.format_exc()
        logger.error(just_the_string)
        logger.exception(error)

    return 'Finished'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
