#Author:xue yi yang
import requests
from lxml import etree
import json
import re
from urllib import parse #解码 url
class get_movie_index():
    # def __init__(self,url = "http://jx.api.163ren.com/vod.php?url=https://v.qq.com/x/cover/70y5f38tjcmtw2t/a0026fc8n8c.html"
    def __init__(self,url
):
        self.head =         head = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        self.url = "http://jx.api.163ren.com/vod.php?url=" + url
    def get_url_key(self):
        """
        获得网址带 key
        :return:
        """
        head = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # url = "http://jx.api.163ren.com/vod.php?url=https://v.qq.com/x/cover/70y5f38tjcmtw2t/a0026fc8n8c.html"
        res = requests.get(url = self.url ,headers=self.head).text
        # return print(res)
        selector = etree.HTML(res)
        url_key = selector.xpath("//script")[4].text

        result = re.findall('url.*', str(url_key))
        # dic = json.dumps(str("{"+result[1]+"}"))
        dic_key = re.findall('\'(.*)\',', str(result[1]))
        # print(type(dic))
        return dic_key[0] #we0NHlkfUTBMZujr08xYMB6CJpyHHzdF3kc/9rU6vYYPjTMpHYU5dYQM4H9F5Ll/TYL1UL8Bl4r3BHfynR8EPKp0oTTc6Ma0x3v0gyDKcin6
    def get_m3u8(self):
        """
        得到url之后，获取m3u8的 返回地址
        :return:
        """
        data = {
            "url" : self.get_url_key(),
            "up":0,
        }
        url = "http://jx.api.163ren.com/api.php"
        res = requests.post(url  = url,headers = self.head,data =data ).text
        return json.loads(res) # json.loads(res) dict 类型
    def get_m3u8_file(self):
        self.get_m3u8()
    def get_renren_m3u8_url(self):
        url  = parse.unquote(self.get_m3u8()["url"])
        # print("url ************",url)
        res = requests.get(url=url ,headers = self.head).text
        """
        res 
        #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=800000,RESOLUTION=1080x452
        /ppvod/316F2512E37A26725B3B703D2AEDF36E.m3u8
        """
        renren_url = "/"+re.findall('/(.*)', str(res))[0]

        return renren_url # /ppvod/316F2512E37A26725B3B703D2AEDF36E.m3u8
    def run(self):
        return self.get_renren_m3u8_url()
        # print(self.get_renren_m3u8_url())
    def if_not_success(self):
        url = parse.unquote(self.get_m3u8()["url"])
        renren_url =   re.findall('(.*)/index.m3u8', str(url))[0]
        # print(renren_url)
        real_url = renren_url+"/1000k/hls/index.m3u8"
        return real_url
if __name__ == '__main__':
    s = get_movie_index("https://v.qq.com/x/cover/fgqtuu38z91hfyw.html")
    s.run()
#     s.if_not_success()

    # url = "https://cn2.zuidadianying.com"