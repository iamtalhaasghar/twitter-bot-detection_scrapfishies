import logging
import sys, os
from logging.handlers import TimedRotatingFileHandler

def get_logger(log_folder, file_name, std_log_level=10, file_log_level=10):

    # create logger
    logger = logging.Logger(None)

    # create console handler and set level to debug
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(std_log_level)
    os.makedirs(log_folder, exist_ok=True)
    # create file handler which logs even debug messages
    fh = TimedRotatingFileHandler(os.path.join(log_folder, file_name), when='midnight')
    fh.setLevel(file_log_level)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(filename)s %(funcName)s:%(lineno)d - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

if __name__=="__main__":
    logger = get_logger('test.log', logging.DEBUG, logging.DEBUG)

    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')