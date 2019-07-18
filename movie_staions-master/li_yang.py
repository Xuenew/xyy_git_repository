import requests
from lxml import etree
import html
url = 'http://www.xueyiyang.top/'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
res = requests.get(url=url,headers=headers).text
#print(res)
selector = etree.HTML(res)
a = selector.xpath("//div/div[2]/text()")
b = selector.xpath("//div/a/@title")
c = zip(b,a)
print(dict(c))


#prt=etree.tostring(a).decode()
#print(prt[0])
#print(a)





















