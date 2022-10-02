import logging
import sys

class Utils:
    def __init__(self):

        self.logger = logging.getLogger()
        self.streamHandler = logging.StreamHandler(sys.stdout)
        self.formatter = logging.Formatter('[%(asctime)s] - %(levelname)s: %(message)s', '%d/%m/%y %H:%M:%S')

    def start_streaming_the_log(self):

        logging.basicConfig(level=logging.DEBUG)
        self.streamHandler.setFormatter(self.formatter)
        self.logger.addHandler(self.streamHandler)
        logging.info("Starting to log the exection")
