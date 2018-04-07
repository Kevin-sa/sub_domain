#encoding: utf-8

#Queries subdonains based on HTTPS certificates

import json
from config import *

class AXFR(object):
    def __init__(self, domain):
        super(AXFR, self).__init__()
        self.domain = domain
        self.address = "https://crt.sh/"
        self.result = []


    def _get(self):
        try:
            url = "{0}?q=%.{1}&output=json".format(self.address, self.domain)
            api_content = get_api_content(url,timeout=50)

            if api_content.status_code != 200:
                logging.error("AXFR get domain fail")

            json_domain = json.loads('[{}]'.format(api_content.text.replace('}{', '},{')))

            for (key,value) in enumerate(json_domain):
                self.result.append(value['name_value'])

            return list(set(self.result))


        except Exception as e:
            #print(e)
            logging.error(str(e))
            return list(self.result)