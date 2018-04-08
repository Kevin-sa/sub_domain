#encoding: utf-8

import dns.resolver, os, sys, gevent, optparse, json, threading, queue,re, itertools
from gevent import monkey
from config import *
from AXFR import AXFR
from dns_zone import Dns_zone

#dictionary and api result subtraction

class Dns_dict(object):

    def __init__(self, domain):
        self.domain = domain
        self.resolver = dns.resolver.Resolver()
        self.resolver.nameservers = dns_servers_default
        self.abspath = os.path.abspath(os.path.dirname(__file__))
        self.threading = 10
        self.result = []


    def _load_sub(self):

        logging.info('[+] loading exited sub dicts')

        domain_sub = []
        sub_file = ['AXFR.json','Dns_zone.json','findsubdomains.json']
        regex = re.compile(r'([A-Za-z0-9]+).{0}'.format(self.domain))

        for i in sub_file:
            absptah = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(absptah,'result/{0}/{1}'.format(self.domain,i))
            #print(file_path)
            with open('{0}'.format(file_path)) as f:
                for lines in f.readlines():
                    if lines:
                        lines = lines.strip().lower()
                        sub_exit = re.findall('(\w+).{0}'.format(self.domain),lines)

                        domain_sub.append(sub_exit)

        domain_sub_exit = itertools.chain(*domain_sub)

        return list(set(domain_sub_exit))

    def _load_dicts(self):

        logging.info('[+] Loading sub dicts')

        domain_sub_exit = self._load_sub()
        domain_dicts = []
        with open('{0}/domain_dicts.txt'.format(self.abspath)) as f:
            for lines in f.readlines():
                #domain are case insensitive
                lines = lines.strip().lower()
                if lines == '':
                    logging.error('domain_dicts is null')
                    continue
                domain_dicts.append(lines)

        domain_dicts = list(set(domain_dicts))

        domain_dicts = list(set(domain_dicts).difference(set(domain_sub_exit)))
        
        return list(domain_dicts)

    def _query(self, sub):
        try:
            target = '{0}.{1}'.format(sub,self.domain)
            answer = self.resolver.query('{0}'.format(target),'A')
            #return answer
            for i in answer.response.answer:
                for j in i.items:
                    if j:
                        return target
        except Exception as e:
            logging.error(str(e))


    def _scan(self):
        dicts = self._load_dicts()
        for sub in dicts:
            subdomain = self._query(sub)
            if subdomain:
                self.result.append(subdomain)
        return list(set(self.result))

