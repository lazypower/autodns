import argparse
from helpers import has_aws_credentials
import logging
from path import Path
from record import Record
from sys import exit


def setup_logging(debug=None, log=None):
    if log:
        log_path = Path(log).expand()
        logging.basicConfig(filename=log_path)
    logger = logging.getLogger('autodns')
    logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    if debug:
        f = '%(asctime)s %(levelname)s %(name)s: %(message)s'
    else:
        f = '%(levelname)s: %(message)s'

    formatter = logging.Formatter(f)
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger


def setup_parser():
    parser = argparse.ArgumentParser(prog='autodns',
                                     description='Update DNS entries on rt53'
                                     ' quickly and easily.')
    parser.add_argument('config',
                        help="Specify configuration file to parse")
    parser.add_argument('-l', '--log', help='log to PATH')
    parser.add_argument('-v', '--debug', action='store_true',
                        help='display debug output')
    return parser


def main(args=None):
    parser = setup_parser()
    known, unknown = parser.parse_known_args(args)
    log = setup_logging(known.debug, known.log)
    log.debug("initialized")
    if not has_aws_credentials():
        exit(1)
    r = Record(known.config)
    r.update()
    log.info('Operation complete')


if __name__ == "__main__":
    main
