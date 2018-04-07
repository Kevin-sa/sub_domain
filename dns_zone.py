#encoding: utf-8

import os, re
from config import *

class Dns_zone(object):
    def __init__(self, domain):
        super(Dns_zone, self).__init__()
        self.domain = domain
        self.result = []

    def _get(self):
        console = os.popen('nslookup -type=ns {0}'.format(self.domain)).read()
        regex = re.compile('nameserver = ([\w\.]+)')
        dns_servers = regex.findall(console)

        for dns_server in dns_servers:
            console = os.popen('dig @{0} axfr {1}'.format(dns_server, self.domain)).read()
            
            regex1 = re.compile('([\w\.]+\.{0})'. format(self.domain))

            #with open('{0}'.format(self.domain)) as file:
            #    file.write(console)

            for value in regex1.findall(console):
                self.result.append(value)

            result = list(set(self.result))

        if len(result) > 0:
            logging.info('Found Dns-Zone-Transfer')
        else:
            logging.error('Not Found Dns-Zone-Transfer')

        return result
