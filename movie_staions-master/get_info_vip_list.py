#Author:xue yi yang
import requests
from lxml import etree
import json
import re
"""  
lxml 的使用方法
res = requests.get(url = self.url ,headers=self.head).text
        # return print(res)
        selector = etree.HTML(res)
        url_key = selector.xpath("//script")[4].text
"""
class get_vip_info_list():
    def __init__(self,page=17):
        self.url = "https://v.qq.com/x/bu/pagesheet/list?_all=2&append=1&channel=movie&listpage=2&offset=0&pagesize=24&sort="+str(page)

        self.head = head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
    }

    def get_items_info(self):
        """
        获取首页的内容 循环 24个div
        :return:
        """
        res = requests.get(url= self.url,headers = self.head).text
        # res = requests.get(url= self.url,headers = self.head)
        # res = requests.get(url= self.url,headers = self.head)

        selector = etree.HTML(res)
        # div_list = selector.xpath("//div[@class='list_item']")
        src_list = selector.xpath("//div[@class='list_item']/a/@href ")
        image_list = selector.xpath("//div[@class='list_item']/a/img[@class='figure_pic']/@src ")
        name_list_no_encode = selector.xpath("//div[@class='list_item']/a/@title ")
        info_list_no_encode = selector.xpath("//div[@class='list_item']/div[@class='figure_detail figure_detail_two_row']/div/@title")
        name_list = []
        info_list = []
        for name in name_list_no_encode:
            name_list.append(name.encode("iso-8859-1").decode('utf8')) # 需要转码 一开始 是 iso-8859-1
        for info  in info_list_no_encode:
            info_list.append(info.encode("iso-8859-1").decode('utf8')) # 需要转码 一开始 是 iso-8859-1
        data_dict = {"src":src_list,"name":name_list,"info":info_list,}
        # return print(div_list,div_list[1],print(res.encode()))
        # return  print(res.encoding)
        data_list = zip(src_list,image_list,name_list,info_list)
        # for i in data_list:
        #     print(i)
        back_list = [i for i in data_list]
        # return back_list
        return back_list
        # return print(div_list)
        # return data_list #data_list 是迭代器形式的 *注意 <element.....>
        #data_list的形式 是[ src,image,name,info] [链接 照片 片名 简要介绍]
# if __name__ == '__main__':
#     s = get_vip_info_list()
#     s.get_items_info()
