#encoding: utf-8

import json, re
from config import *

class Findsubdomains(object):

    def __init__(self, domain):
        super(Findsubdomains, self).__init__()
        self.domain = domain
        self.address = "https://findsubdomains.com/subdomains-of"
        self.result = []


    def _get(self):
        try:
            url = "{0}/{1}".format(self.address, self.domain)
            api_content = get_api_content(url)

            if api_content.status_code != 200:
                logging.error("findsubdomains get domain fail")

            regex = re.compile(r'([a-zA-Z0-9]+.{0})'.format(self.domain))
            for value in regex.findall(api_content.text):
                self.result.append(value)


            return list(set(self.result))

        except Exception as e:
            logging.error(str(e))
            return self.result
