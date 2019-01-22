# log any parameters passed by URL

import logging
import time

from flask import Flask, request

app = Flask(__name__)

# Configure logging with timestamp and log level. Name the log file by date.
# print(app.logger)
# print(dir(app.logger))
# print(type(app.logger))

''' Normal logging config, does not work in PythonAnywhere.
configed_logger = logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                        level=logging.DEBUG,
                        filename=time.strftime('%Y_%m_%d') + '.log',
                        filemode='a+')
'''

# Since PythonAnywhere does special server logging, we need to grab the logger that is already configured:
# This solution doesn't work locally for some reason. It creates the files, but doesn't write to them.
logfile_handler = logging.FileHandler(time.strftime('%Y_%m_%d') + '.log')
logfile_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(message)s'))
logfile_handler.setLevel(logging.DEBUG)
logger = logging.getLogger()
logger.addHandler(logfile_handler)


# print(configed_logger)

@app.route('/')
def log_params():
    logger.info(request.args)
    logger.info(dir(request.args))
    logger.info(list(request.args))
    logger.info(request.args.__repr__())
    return 'Unauthorized'


if __name__ == '__main__':
    app.run()
    # app.run(host='127.0.0.1',port=8000,debug=True)
