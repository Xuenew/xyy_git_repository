#Author:xue yi yang

# coding: utf-8

# In[1]:


import requests
import json
import time
import hashlib
import re


# In[2]:


def getckey(vid, platform):
    tm = str(int(time.time()))
    string = "4244ce1b{}{}*#06#10201".format(vid, tm)  # encryptVer=7.2
    ckey = hashlib.md5(string.encode('utf-8')).hexdigest()
    flowid = "{}_{}".format(hashlib.md5(tm.encode('utf-8')).hexdigest(), platform)
    return tm, ckey, flowid


# In[3]:


def proxyhttp(url, data):
    s = requests.Session()
    s.headers.update({
                         "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"})
    s.headers.update({"referer": url})

    cookie = "pgv_pvi=6886795264; RK=gXTYpKgRwG; ptcz=840f92f9f159c3df7426ee93de8db40f2aac5846024c670da50da72b38a86f57; tvfe_boss_uuid=262d9f7357466816; pgv_pvid=8810885929; appuser=2C6DD715C20A4FB4; o_minduid=Noo0SV5hPDmrM_BmezZCjIcb4bNOwtc4; pt2gguin=o1287986063; eas_sid=c1g5k3c8d5z7F5C4i3B53815G4; _ga=GA1.2.1401926032.1538576269; o_cookie=1287986063; pac_uid=1_1287986063; pgv_info=ssid=s8691309488; psessionid=753b52bb_1550913690_1287986063_12868; cm_cookie=V1,110061&f1288a4ca44809f&AQEBReuUsErVKO8APUl7x9H9JoazHP3ft5Ph&180512&180512,10008&86DB7F117302411B942DE9A135EFFC3C-&AQEB3hf315d9Rk3WQmRWuNyG_YZXovagHuzH&180713&180731,10027&1531474496603987&AQEB2ESdf26LlMkv98aJjckezs8GkNRPG7Z7&180804&180804,110055&s0187af75df41bf1e2d&AQEBU7cLHFaTfVzcidOZUVYR0gzgFzFMxGyg&180805&181107,110120&5766185851548174655&AQEBECEEbOnrSf1NHv6oSmOUJwqPHG0-KQ2N&181108&181108,10016&G1LIOs21cjIy&AQEBpTlkJymSFeYmP6Y6TXNrKSbRVBImQJEY&180805&181111,110080&EC38C46F0E2D575B42BED2&AQEBECEEbOnrSf1GI3MmVjN-WLK_w9arUl_U&190120&190223,110066&64zAf0jc0750&AQEBECEEbOnrSf27J43ybvHWRCigUfy8hBaX&180820&190223,110065&6sNjZU62Wq&AQEBECEEbOnrSf3IL-0efraLbw9tW67oyrkk&180820&190223; adid=1287986063; LHTturn=582; image_md5=3c32a8e53f5bdbc2652e06e3aaa9cb3e; ufc=r47_1_1551002765_1550916545; LZTturn=49; lv_play_indexl.=72; psessiontime=1550916479; Lturn=217; LPLFturn=10; LKBturn=749; LPVLturn=84; LVMturn=508; LPSJturn=156; LBSturn=273; LZIturn=665; LZCturn=258; LCZCturn=914; LVINturn=660"
    c = {}
    for _ in cookie.split(';'):
        key, value = _.strip().split('=', 1)
        c.update({key: value})
    requests.utils.add_dict_to_cookiejar(s.cookies, c)
    r = s.post("https://vd.l.qq.com/proxyhttp", data=data)
    return (r)


# In[4]:


def getdata(url, vid, coverid, guid, unid, sdtfrom):
    platform = ["10201"]
    tm, ckey, flowid = getckey(vid, platform[0])
    defn = ["fhd", "shd", "hd", "sd"]
    data = {
        "buid": "onlyvinfo",
        "vinfoparam": "charge=0&defaultfmt=auto&otype=ojson&guid={}&flowid={}"
                      "&platform=10201&sdtfrom=v1010&defnpayver=1&appVer=3.5.56&host=v.qq.com"
                      "&ehost={}&refer=v.qq.com&sphttps=1&tm={}&spwm=4&unid={}&vid={}&defn={}"
                      "&fhdswitch=1&show1080p=1&isHLS=1&onlyGetinfo=true&dtype=3&sphls=2&spgzip=1"
                      "&dlver=2&defsrc=2&encryptVer=7.2&cKey={}&fp2p=1".format(guid, flowid, url, tm, unid, vid, 'fhd',
                                                                               ckey)
    }
    return json.dumps(data)


# In[5]:


def getid(url):
    mode = [
        '.*v\.qq\.com/x/cover/(.*)\.html\?vid=(.*)',
        '.*v\.qq\.com/x/cover/(.*)/(.*)\.html',
        '.*v\.qq\.com/x/page/(.*)\.html',
    ]
    for _ in mode:
        matchres = re.match(_, url)
        if matchres == None:
            pass
        else:
            matchres = matchres.groups()
            vid = matchres[-1]
            if len(matchres) == 2:
                coverid = matchres[0]
            else:
                coverid = ""
    return vid, coverid


# In[6]:


def dl_qq(url):
    guid = "5ab01a7ab3b68b62787b5d1df507ba5c"  # 固定值
    unid = "1cbe987dbf1111e89d19a0424b63310a"  # 也是一个固定值
    sdtfrom = "v1010"
    # url = "https://v.qq.com/x/cover/y4g7p8eka7bshz3/i0544naygqq.html"
    vid, coverid = getid(url)
    # vid = "w00273lvxjp"
    # coverid = "0913mhn6zhnk66b"
    data = getdata(url, vid, coverid, guid, unid, sdtfrom)
    res = proxyhttp(url, data)
    resdict = json.loads(res.content.decode('utf-8'))
    print("**********************",resdict)
    resdict.get("errCode")
    if resdict.get("errCode") == 0:
        pass
    else:
        print(resdict.get("errCode"))
    resdict = json.loads(resdict["vinfo"])['vl']['vi'][0]
    title = re.sub('[\/:*?"<>|]', '', resdict.get("ti"))
    urllist = resdict.get("ul").get("ui")
    m3u8_url = urllist[-1].get("url")
    type = "m3u8"
    if ".m3u8" in m3u8_url:
        pass
    else:
        m3u8_url = m3u8_url + urllist[-1].get("hls").get("pt")
    screensize = "{}x{}".format(resdict.get("vw"), resdict.get("vh"))
    try:
        vkey = resdict["fvkey"]
    except KeyError:
        urllist = [m3u8_url]
        print(title, screensize)
        print(m3u8_url)
    else:
        type = "list"
        urllist = []
        if len(resdict["cl"]["ci"]) == 1:
            keyid = resdict["cl"]["ci"][0]["keyid"]
            keyid = keyid.replace(".10", ".p")
            directlink = "{}{}.mp4?sdtfrom={}&guid={}&vkey={}".format(m3u8_url, keyid, sdtfrom, guid, vkey)
            print(directlink)
            urllist.append(directlink)
        else:
            pass
    dlinfo = {"title": title, "url": urllist, "type": type, "referer": "https://v.qq.com"}
    print(dlinfo)
    return dlinfo


def main():
    # url = input("请输入链接：\n")
    url = "https://v.qq.com/x/cover/y4g7p8eka7bshz3/i0544naygqq.html"
    dl_qq(url)


if __name__ == "__main__":
    main()