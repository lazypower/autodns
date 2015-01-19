import logging
from IPy import IP
from os import environ
from path import Path
from requests import get
import yaml

CACHE_PATH = '~/.autodns.cache'
log = logging.getLogger('autodns')


def get_host_ip():
    """ Call out to icanhazip for the host ip address """
    response = get('http://icanhazip.com')
    # Validate that we got an IP and not a status 500 page
    ip = IP(response.text)
    # Return the string representation of the IP
    return str(ip)


def ip_has_changed(ip, config):
    current_ip = ip
    # Handle cases where we haven't initialized
    # anything with autodns
    if 'ADDRESS' not in config.keys():
        return False
    old_ip = config['ADDRESS']
    if current_ip == old_ip:
        return False
    return True


def read_config(config):
    config_path = Path(config)
    if config_path.exists():
        with open(config_path, 'r') as f:
            cfg = yaml.safe_load(f.read())
        return cfg
    else:
        msg = "Non existant configuration: {}".format(config_path)
        log.critical(msg)
        raise OSError(msg)


def write_config(config, record):
    config_path = Path(config)
    if config_path.exists():
        with open(config_path, 'w') as f:
            f.write(yaml.dump(record))
    return record.keys()


def aws_keys():
    secret = environ.get('AWS_SECRET_ACCESS_KEY')
    key = environ.get('AWS_ACCESS_KEY_ID')
    return (key, secret)


def has_aws_credentials():
    secret = environ.get('AWS_SECRET_ACCESS_KEY')
    key = environ.get('AWS_ACCESS_KEY_ID')
    if not secret:
        log.critical('Missing environment variable AWS_SECRET_ACCESS_KEY')
        return False
    if not key:
        log.critical('Missing environment variable AWS_ACCESS_KEY_ID')
        return False
    return True
