#Author:xue yi yang
import requests
import ssl
from lxml import etree
ssl._create_default_https_context = ssl._create_unverified_context

#获取当前访问使用的IP地址网站
url="https://www.ipip.net/"

#设置代理，从西刺免费代理网站上找出一个可用的代理IP
proxies={'http': '222.74.61.98:53281',} #此处也可以通过列表形式，设置多个代理IP，后面通过random.choice()随机选取一个进行使用

#使用代理IP进行访问
headers ={
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
}

res=requests.get(url,proxies=proxies,headers=headers)
status=res.status_code # 状态码
print(status)
content=res.text
html=etree.HTML(content)
ip=html.xpath('//ul[@class="inner"]/li[1]/text()')[0]
print("当前请求IP地址为："+ip)
