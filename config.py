#encoding: utf-8

from random import choice
import logging
import requests as requests

#default DNS server
dns_servers_default = ['114.114.114.114','223.5.5.5']

#Randomly generated User-Agent
#choice(User_Agent)

#User-Agent in hhtp header
User_Agent = [
"Mozilla/5.0 (Windows; U; Windows NT 6.0; cs; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13",
"Mozilla/5.0 (Windows; U; Windows NT 6.0; cs; rv:1.9.0.19) Gecko/2010031422 Firefox/3.0.19",
"Opera 9.4 (Windows NT 5.3; U; en)",
"Opera 9.4 (Windows NT 6.1; U; en)",
"Opera/9.64 (X11; Linux i686; U; pl) Presto/2.1.1",
]


#Set http request header
headers = {
    'User-Agent' : choice(User_Agent),
    'Referer' : '',
    'Cookie' : '',
}


#console output log
logging.basicConfig(level = logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')


#requests api_url
def get_api_content(url, timeout='' ,cookie=""):
    try:
        if cookie:
            headers['Cookie'] = cookie
        if timeout:
            timeout = timeout
        else:
            timeout = 5
        content = requests.get(url,
                               headers = headers,
                               timeout =timeout
                               )
        return content
    except ConnectionError as e:
    #   print(e)
       logging.error(str(e))