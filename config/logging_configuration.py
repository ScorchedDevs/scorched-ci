# pylint: disable=too-few-public-methods
import logging
import sys


def config_logger():

    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s]: %(message)s",
        stream=sys.stdout,
    )
