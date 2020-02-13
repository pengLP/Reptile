"""
刷csdn访问量
"""
import re
import time
import random
import requests
import urllib.request
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

IPRegular = r"(([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5]).){3}([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5])"

host = "https://blog.csdn.net"
url = "https://blog.csdn.net/qq_36008321/article/details/{}"


def parseIPList(url="http://www.xicidaili.com/"):
    IPs = []
    request = urllib.request.Request(url, headers={'User-Agent': UserAgent().random})
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response, "html.parser")
    tds = soup.find_all("td")
    for td in tds:
        string = str(td.string)
        if re.search(IPRegular, string):
            IPs.append(string)
    return IPs


def parseArticleList(url):
    article = []
    request = urllib.request.Request(url, headers={'User-Agent': UserAgent().random})
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response, "html.parser")
    lists = soup.find_all('div', attrs={'class': 'article-item-box csdn-tracking-statistics'})
    for i in lists:
        if (i['data-articleid'] is not None):
            article.append(i['data-articleid'])
    return article


def PV(code):
    IPs = parseIPList()
    proxy = {"http": "{}:8080".format(IPs[random.randint(0, len(IPs) - 1)])}
    try:
        r = requests.get(url.format(code), headers={'User-Agent': UserAgent().random}, proxies=proxy, timeout=30)
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("getHTML error")
        return "error"



if __name__ == '__main__':
    # print(parseIPList())
    codes = parseArticleList("https://blog.csdn.net/qq_36008321")
    count = 0
    while True:
        count += 1
        print("正在进行第{}次访问\t".format(count), end="\t")
        res = PV(codes[random.randint(0, len(codes) - 1)])
        time.sleep(random.randint(30, 60))
