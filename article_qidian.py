import requests
import re
from bs4 import BeautifulSoup
from requests.exceptions import *
import random
import json
import time
import os
import chardet

def random_user_agent():
    list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36']
    seed = random.randint(0, len(list) - 1)
    return list[seed]


def getJson(id):
    url = 'https://book.qidian.com/ajax/book/category?csrfToken=BXnzDKmnJamNAgLu4O3GknYVL2YuNX5EE86tTBAm&bookId='+id
    headers = {'User-Agent': random_user_agent(),
               'Referer': 'https://book.qidian.com/info/'+id,
               'Cookie': '_csrfToken=BXnzDKmnJamNAgLu4O3GknYVL2YuNX5EE86tTBAm; newstatisticUUID=1564467217_1193332262; qdrs=0%7C3%7C0%7C0%7C1; showSectionCommentGuide=1; qdgd=1; lrbc=1013637116%7C436231358%7C0%2C1003541158%7C309402995%7C0; rcr=1013637116%2C1003541158; bc=1003541158%2C1013637116; e1=%7B%22pid%22%3A%22qd_P_limitfree%22%2C%22eid%22%3A%22qd_E01%22%2C%22l1%22%3A4%7D; e2=%7B%22pid%22%3A%22qd_P_free%22%2C%22eid%22%3A%22qd_A18%22%2C%22l1%22%3A3%7D'
               }
    try:
        res = requests.get(url=url, params=headers)
        if res.status_code == 200:
            json_str = res.text
            list = json.loads(json_str)['data']['vs']
            response = {
                'VolumeId_List': [],
                'VolumeNum_List': []
            }
            for i in range(len(list)):
                json_str = json.dumps(list[i]).replace(" ", "")
                volume_id = re.search('.*?"vId":(.*?),', json_str, re.S).group(1)
                volume_num = re.search('.*?"cCnt":(.*?),', json_str, re.S).group(1)
                response['VolumeId_List'].append(volume_id)
                response['VolumeNum_List'].append(volume_num)
            return response
        else:
            print('No response')
            return None
    except ReadTimeout:
        print("ReadTimeout!")
        return None
    except RequestException:
        print("请求页面出错！")
        return None


def getPage(VolId_List, VolNum_List,id):
    '''
    通过卷章Id找到要爬取的页面，并返回页面html信息
    :param VolId_List: 卷章Id列表
    :param VolNum_List: 每一卷含有的章节数量列表
    :return:
    '''
    size = len(VolId_List)
    for i in range(size):
        path = str(i + 1)
        mkdir(path)
        url = 'https://read.qidian.com/hankread/'+id+'/' + VolId_List[i]
        print('\n当前访问路径：' + url)
        headers = {
            'User-Agent': random_user_agent(),
            'Referer': 'https://book.qidian.com/info/'+id,
            'Cookie': 'e1=%7B%22pid%22%3A%22qd_P_hankRead%22%2C%22eid%22%3A%22%22%2C%22l1%22%3A3%7D; e2=%7B%22pid%22%3A%22qd_P_hankRead%22%2C%22eid%22%3A%22%22%2C%22l1%22%3A2%7D; _csrfToken=BXnzDKmnJamNAgLu4O3GknYVL2YuNX5EE86tTBAm; newstatisticUUID=1564467217_1193332262; qdrs=0%7C3%7C0%7C0%7C1; showSectionCommentGuide=1; qdgd=1; e1=%7B%22pid%22%3A%22qd_P_limitfree%22%2C%22eid%22%3A%22qd_E01%22%2C%22l1%22%3A4%7D; e2=%7B%22pid%22%3A%22qd_P_free%22%2C%22eid%22%3A%22qd_A18%22%2C%22l1%22%3A3%7D; rcr=3144877%2C1013637116%2C1003541158; lrbc=3144877%7C52472447%7C0%2C1013637116%7C436231358%7C0%2C1003541158%7C309402995%7C0; bc='+id
        }
        try:
            res = requests.get(url=url, params=headers)
            if res.status_code == 200:
                print('第' + str(i + 1) + '卷已开始爬取：')
                parsePage(res.text, url, path, int(VolNum_List[i]))
            else:
                print('No response')
                return None
        except ReadTimeout:
            print("ReadTimeout!")
            return None
        except RequestException:
            print("请求页面出错！")
            return None
        time.sleep(3)


def parsePage(html, url, path, chapNum):
    '''
    解析小说内容页面，将每章内容写入txt文件，并存储到相应的卷目录下
    :param html: 小说内容页面
    :param url: 访问路径
    :param path: 卷目录路径
    :return: None
    '''
    if html == None:
        print('访问路径为' + url + '的页面为空')
        return
    soup = BeautifulSoup(html, 'html.parser')
    ChapInfoList = soup.find_all('div', attrs={'class': 'main-text-wrap'})
    alreadySpiderNum = 0.0
    for i in range(len(ChapInfoList)):
        print('\r已爬取{0}'.format('%.2f%%' % float(alreadySpiderNum / chapNum * 100)))
        time.sleep(0.5)
        soup1 = BeautifulSoup(str(ChapInfoList[i]), 'html.parser')
        ChapName = soup1.find('h3', attrs={'class': 'j_chapterName'}).span.string
        ChapName = re.sub('[\/:*?"<>|]', '', ChapName)
        if ChapName == '无题':
            ChapName = '第' + str(i + 1) + '章 无题'
        filename = path + '//' + ChapName + '.txt'
        readContent = soup1.find('div', attrs={'class': 'read-content j_readContent'}).find_all('p')
        for item in readContent:
            paragraph = re.search('.*?<p>(.*?)</p>', str(item), re.S).group(1)
            save2file(filename, paragraph)
        alreadySpiderNum += 1.0
    print('\r已爬取{0}'.format('%.2f%%' % float(alreadySpiderNum / chapNum * 100)))


def save2file(filename, content):
    with open(r'' + filename, 'a', encoding='utf-8') as f:
        f.write(content + '\n')
        f.close()


def mkdir(path):
    '''
    创建卷目录文件夹
    :param path: 创建路径
    :return: None
    '''
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
    else:
        print('路径' + path + '已存在')


def main():
    id = "1014264950"
    response = getJson(id)
    if response != None:
        VolId_List = response['VolumeId_List']
        VolNum_List = response['VolumeNum_List']
        getPage(VolId_List, VolNum_List,id)
    else:
        print('无法爬取该小说！')
    print("小说爬取完毕!")


if __name__ == '__main__':
    main()