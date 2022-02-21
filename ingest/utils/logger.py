import logging
import sys


def init_logger():
    my_logger = logging.getLogger()
    my_logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)

    fh = logging.FileHandler('logs.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    my_logger.addHandler(fh)
    my_logger.addHandler(sh)
    return my_logger


logger = init_logger()
