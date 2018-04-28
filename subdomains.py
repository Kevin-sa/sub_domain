#encoding: utf-8

import os, json, argparse, re
from AXFR import AXFR
from dns_zone import Dns_zone
from findsubdomains import Findsubdomains
from dns_dict import Dns_dict
from config import *


def out_file(file_path, filename, result):
    result_file = os.path.join(file_path, filename)
    try:
        fd = open(result_file, 'w')
        json.dump(result, fd , indent=4)
    finally:
        fd.close()


def run(args):
    domain = args.domain
    if not domain:
        logging.error("input the target")
        exit(1)

    regex = re.compile(r'(([a-zA-Z0-9]+){1,1}\.[A-Za-z]+)')
    if not regex.match(domain):
        logging.error("inputh the right domain")
        exit(1)

    file_abspath = os.path.dirname(os.path.abspath(__file__))
    mkdir_path = os.path.join(file_abspath, 'result/{0}'.format(domain))
    if not os.path.exists(mkdir_path):
        os.makedirs(mkdir_path)

    #AXFR
    logging.info("starting AXFR...")
    result = AXFR(domain)._get()
    out_file(mkdir_path, 'AXFR.json', result)
    logging.info("Finish AXFR")

    #Dns_zone
    logging.info("starting Dns_zone...")
    result = Dns_zone(domain)._get()
    out_file(mkdir_path, 'Dns_zone.json', result)
    logging.info("Finish Dns_zone")

    #findsubmains
    logging.info("starting findsubdomains...")
    result = Findsubdomains(domain)._get()
    out_file(mkdir_path, 'findsubdomains.json', result)
    logging.info('Finish findsubdomains.json')

    #hackertarget
    logging.info("starting hacktarget...")
    result = Hackertarget(domain)._get()
    out_file(mkdir_path, 'hackertarget.json', result)
    logging.info('Finish findsubdomains.json')

    #sub_dicts
    #dictionary and api result subtraction
    logging.info("starting dicts")
    result = Dns_dict(domain)._run()
    out_file(mkdir_path, 'dict_sub.json', result)
    logging.info('Finish dict_sub.json')

    #result
    file_exits = os.listdir(mkdir_path)
    for i in file_exits:
        print("[+] {0}".format(i))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'subdomains.py', usage='%(prog)s [options] [args] usage', description='subdomains-a v-0.1')
    #parser.print_help()
    parser.add_argument("-d", dest="domain",type=str, help="-d target,default out_file in 'result' file")

    args = parser.parse_args()

    try:
        run(args)
    except Exception as e:
        logging.error(str(e))
        exit(1)









