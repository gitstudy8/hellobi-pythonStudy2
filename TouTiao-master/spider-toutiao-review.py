import requests
import re
from urllib.parse import urlencode
from requests.exceptions import RequestException
import json
from bs4 import BeautifulSoup
import pymongo
from hashlib import md5
import os
from multiprocessing.dummy import Pool
from json import JSONDecodeError

from config import *

# client=pymongo.MongoClient(MONGO_URL)
client=pymongo.MongoClient(MONGO_URL,connect=False)
db=client[MONGO_DB]

def get_page_index(offset,keyword):
    data={
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3
    }
    url='https://www.toutiao.com/search_content/?' + urlencode(data)
    # print(url)
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错！')
        return None
#
# def parse_page_index(html):
#     data=json.loads(html)
#     if data and 'data' in data.keys():###判断data中是否含有我们要的数
#         for item in data.get('data'):
#             yield item.get('article_url')

###html为空的时候，以上语句报错，所以加判断
def parse_page_index(html):
    try:
        data=json.loads(html)
        if data and 'data' in data.keys():###判断data中是否含有我们要的数
            for item in data.get('data'):
                yield item.get('article_url')
    except JSONDecodeError:
        pass
def get_page_detail(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错！')
        return None
###解析详情页
def parse_page_detail(html,url):
    soup=BeautifulSoup(html,'lxml')
    title=soup.select('title')[0].get_text()
    print(title)
    ##有多个，会报错
    images_pattern=re.compile('gallery:(.*?)siblingList',re.S)
    result=re.search(images_pattern,html)
    # return result.group(1)
    if result:
        # print(result.group(1))
        # return result.group(1).strip().strip(',')
        data=json.loads(result.group(1).strip().strip(','))
        if data and 'sub_images' in data.keys():
            sub_images=data.get('sub_images')
            #遍历，提取图片url，用列表形式展现，一句话构造出一个列表
            images=[item.get('url')  for item in sub_images]
            #########调用、下载图片
            for image in images:download_imgage('http:'+image)
            # for image in images:print('http:'+image)
            #########调用、下载图片
            return {
                'title':title,
                'url':url,
                'images':images
            }


def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到MongoDB成功',result)
        return True
    return False

def download_imgage(url):
    print('正在下载',url)
    try:
        response=requests.get(url)
        if response.status_code==200:
            save_img(response.content)
            #response.text返回网页，response.content返回二进制
            # return response.text
        return None
    except RequestException:
        print('请求图片出错！')
        return None

def save_img(content):
    # os.mkdir("img")
    file_path='{0}/{1}.{2}'.format(os.getcwd()+'.\\img',md5(content).hexdigest(),'jpg')
    ###md5防止下载重复图片，相同图片MD5相同
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()



#
# def main():
#     html=get_page_index(0,'街拍')
#     for url in parse_page_index(html):
#         html=get_page_detail(url)
#         print(url)
#         if html:
#             result=parse_page_detail(html,url)
#             print(result)
#             save_to_mongo(result)

def main(offset):
    html=get_page_index(offset,KEYWORD)
    for url in parse_page_index(html):
        html=get_page_detail(url)
        print(url)
        if html:
            result=parse_page_detail(html,url)
            print(result)
            # save_to_mongo(result)
            # 如果出错，可以加一个判断，只有有数据才保存
            if result:save_to_mongo(result)

if __name__ == '__main__':
    # main()
    groups=[x*20 for x in range(GROUP_START, GROUP_END+1)]
    #构造list
    ###多进程
    pool=Pool()
    pool.map(main, groups)
