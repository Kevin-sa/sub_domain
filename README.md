# sub_domain

利用API查询目标子域名、利用DNS区域泄露查找目标子域名，并于字典取差积再爆破获得目标最终的子域名列表

### Use
subdomain.py -d target.com
```
python3 subdomains.py -h
usage: subdomains.py [options] [args] usage

subdomains-a v-0.1

optional arguments:
  -h, --help  show this help message and exit
  -d DOMAIN   -d target,default out_file in 'result' file
```

### result
结果保存在result/target/
```
root@ubuntu:/home/kevinsa/PycharmProjects/domain# tree result/
result/
├── alipay.com
│   ├── AXFR.json
│   ├── dict_sub.json
│   ├── Dns_zone.json
│   └── findsubdomains.json
├── hncc.edu.cn
│   ├── AXFR.json
│   ├── dict_sub.json
│   ├── Dns_zone.json
│   └── findsubdomains.json
└── weibo.com
    ├── AXFR.json
    ├── dict_sub.json
    ├── Dns_zone.json
    └── findsubdomains.json
```

### 1.API查询目标子域名
#### 1.1AXFR
AXFR.py
https://crt.sh/

#### 1.2 findsubdomains
findsubdomains.py
https://findsubdomains.com/subdomains-of

#### 2.DNS zone transfer
```
; <<>> DiG 9.10.3-P4-Ubuntu <<>> @dns2.hncc.edu.cn axfr hncc.edu.cn
; (1 server found)
;; global options: +cmd
hncc.edu.cn.    	86400	IN	SOA	dns.hncc.edu.cn. root.hncc.edu.cn. 2018012300 28800 14400 3600000 86400
hncc.edu.cn.		86400	IN	MX	5 mail.hncc.edu.cn.
hncc.edu.cn.		86400	IN	MX	10 mail1.hncc.edu.cn.
hncc.edu.cn.		86400	IN	NS	dns.hncc.edu.cn.
hncc.edu.cn.		86400	IN	NS	dns2.hncc.edu.cn.
```
#### 3.字典爆破
将字典保存为domain_dicts.txt，将取字典与API、DNS zone transfer的差积爆破

#### 等待更新......
* 字典爆破泛解析问题
    * 思路1：dns.resolver.query()请求一个不可能存在的子域名并于字典内域名查询结果对比；
```
    try:
            pan_parsing = 'subdoamin-aaa.{}'.format(self.domain)
            pan_answer = self.resolver.query(pan_parsing, 'A')
            for i in pan_answer.response.answer:
                if len(i)>0:
                    logging.error("exit pan-parsing")
                    return
        except:
            pass
```
    *~~思路2：字典完成后，随机获取5个子域名进行http请求判断  ~
* ~~字典爆破线程
    * ```queue.Queue threading.Thread()```~~


#### 项目参考
https://github.com/ring04h/wydomain

