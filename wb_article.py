from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
import time

base_url = 'https://m.weibo.cn/api/container/getIndex?' 

headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

def get_page(page): #得到页面的请求，params是我们要根据网页填的，就是下图中的Query String里的参数
    params = {
        'containerid': '100103type=1&q=电视剧',
        'page': page,#page是就是当前处于第几页，是我们要实现翻页必须修改的内容。
        'type':'all',
        'queryVal':'电视剧',
        'featurecode':'20000320',
        'luicode':'10000011',
        'lfid':'106003type=1',
        'title':'电视剧'
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(page) 
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)

def parse_page(json):
    if json:
        res = []
        items = json.get('data').get('cards')
        for i in items:
            if i == None:
                continue
            item = i.get('mblog')
            if item == None:
                continue
            weibo = {}
            weibo['id'] = item.get('id')
            weibo['text'] = pq(item.get('text')).text()
            weibo['name'] = item.get('user').get('screen_name')
            if item.get('longText') != None :#要注意微博分长文本与文本，较长的文本在文本中会显示不全，故我们要判断并抓取。
                weibo['longText'] = item.get('longText').get('longTextContent')
            else:weibo['longText'] =None
            weibo['attitudes'] = item.get('attitudes_count')
            weibo['comments'] = item.get('comments_count')
            weibo['reposts'] = item.get('reposts_count')
            weibo['time'] = item.get('created_at')
            res.append(weibo)
        return res
if __name__ == '__main__':
    for page in range(21,200):#循环页面
        time.sleep(1)         #设置睡眠时间，防止被封号
        json = get_page(page)
        results = parse_page(json)
        print(results)

