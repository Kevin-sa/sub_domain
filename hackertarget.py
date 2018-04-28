#encodeing:utf-8

import json, re
from config import *

class Hackertarget(object):

    def __init__(self,domain):
        self.domain = domain
        self.address = 'http://api.hackertarget.com/hostsearch/?q='
        self.result = []

    def _get(self):
        try:
            url = '{0}{1}'.format(self.address,self.domain)
            api_content = get_api_content(url)

            if api_content.status_code != 200:
                logging.error("hackertaget get domain fail")

            regex = re.compile(r'([a-zA-Z0-9]+.{0})'.format(self.domain))
            for value in regex.findall(api_content.text):
                self.result.append(value)

            return list(set(self.result))

        except Exception as e:
            print(str(e))
            return self.result

