# pylint: disable=too-few-public-methods
import logging
import sys


class Utils:
    def __init__(self):

        self.logger = logging.getLogger()
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.formatter = logging.Formatter(
            "[%(asctime)s] - %(levelname)s: %(message)s", "%d/%m/%y %H:%M:%S"
        )

    def start_streaming_the_log(self):

        logging.basicConfig(level=logging.INFO)
        self.stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.stream_handler)
        logging.info("Starting to log the exection")
