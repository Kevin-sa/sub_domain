#encoding: utf-8

import dns.resolver, os, sys,  optparse, json, threading, queue,re, itertools
from config import *


#dictionary and api result subtraction

class Dns_dict(object):

    def __init__(self, domain):
        self.domain = domain
        self.resolver = dns.resolver.Resolver()
        self.resolver.nameservers = dns_servers_default
        self.abspath = os.path.abspath(os.path.dirname(__file__))
        self.threading = 10
        self.result = []
        self.sub_dict = queue.Queue()


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
                #if lines == '':
                #    logging.error('domain_dicts is null')
                #    continue
                domain_dicts.append(lines)

        domain_dicts = list(set(domain_dicts))
        domain_dicts = list(set(domain_dicts).difference(set(domain_sub_exit)))
        for sub_dicts in domain_dicts:
            self.sub_dict.put(sub_dicts)

        return True

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
        while not self.sub_dict.empty():
            sub = self.sub_dict.get()
            subdomain = self._query(sub)
            if subdomain:
                self.result.append(subdomain)


    def _run(self):
        
        try:
            pan_parsing = 'subdoamin-aaa.{}'.format(self.domain)
            pan_answer = self.resolver.query(pan_parsing, 'A')
            for i in pan_answer.response.answer:
                if len(i)>0:
                    logging.error("exit pan-parsing")
                    return
        except:
            pass

        self._load_sub()
        self._load_dicts()
        for i in range(self.threading):
            t = threading.Thread(target=self._scan())
            t.start()
            t.join()

        return list(set(self.result))

