"""
刷csdn访问量
"""
import re
import time
import random
import requests
import urllib.request
from bs4 import BeautifulSoup

IPRegular = r"(([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5]).){3}([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5])"

host = "https://blog.csdn.net"
url = "https://blog.csdn.net/qq_36008321/article/details/{}"

def random_user_agent():
    list = [
        {"User-Agent": 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36'},
        {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'},
        {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36'},
        {"User-Agent": 'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36'},
        {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36'}]
    seed = random.randint(0, len(list) - 1)
    return list[seed]


def parseIPList(url="http://www.xicidaili.com/"):
    IPs = []
    request = urllib.request.Request(url, headers=random_user_agent())
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
    request = urllib.request.Request(url, headers=random_user_agent())
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response , "html.parser")
    lists = soup.find_all('div' , attrs={'class':'article-item-box csdn-tracking-statistics'})
    for i in lists:
        if (i['data-articleid'] is not None) :
            article.append(i['data-articleid'])
    return article


def PV(code):
    s = requests.Session()
    s.headers = random_user_agent()
    IPs = parseIPList()
    s.proxies = {"http": "{}:8080".format(IPs[random.randint(0, 40)])}
    s.get(host)
    r = s.get(url.format(code))
    return url.format(code)

if __name__ == '__main__':
    print(parseIPList())
    codes = parseArticleList("https://blog.csdn.net/qq_36008321")
    count = 0
    while(True):
        count += 1
        print("正在进行第{}次访问\t".format(count), end="\t")
        print(PV(codes[random.randint(0, len(codes) - 1)]))
        time.sleep(random.randint(60, 75))
