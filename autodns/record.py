from boto import route53
import logging

from .helpers import aws_keys
from .helpers import get_host_ip
from .helpers import has_aws_credentials
from .helpers import read_config
from .helpers import write_config

log = logging.getLogger('autodns')


class Record:

    def __init__(self, cfg):
        if not has_aws_credentials():
            raise ValueError("Unable to locate AWS credentials. See README")
        self.config = cfg
        config = read_config(cfg)
        self.ip = get_host_ip()
        self.accesskey, self.secret = aws_keys()
        self.domains = config['DOMAINS']
        self.ttl = config['TTL']
        self.zoneid = config['ZONEID']
        # Fix for #1
        self.address = ''
        if 'ADDRESS' in config.keys():
            self.address = config['ADDRESS']

    def update(self):
        if self.ip == self.address:
            # No change required
            log.info("No Change Required - Exiting")
            return
        conn = route53.connection.Route53Connection(self.accesskey,
                                                    self.secret)
        rrs = route53.record.ResourceRecordSets(conn, self.zoneid,
                                                comment='rt53-autodns')
        # boto has really strange syntax that mandates the format below
        for domain in self.domains:
            change = rrs.add_change(action='UPSERT', name=domain, type='A',
                                    ttl=self.ttl)
            change.add_value(self.ip)
        commit_result = rrs.commit()
        log.info(commit_result)
        write_config(self.config, self.keys())

    def keys(self):
        return {'ADDRESS': self.ip,
                'DOMAINS': self.domains,
                'TTL': self.ttl,
                'ZONEID': self.zoneid}
