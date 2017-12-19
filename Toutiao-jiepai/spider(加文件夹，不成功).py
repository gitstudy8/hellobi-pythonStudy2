import os
import re
import pymongo
import requests
from urllib.parse import  urlencode
from hashlib import md5

from bs4 import BeautifulSoup
from requests.exceptions import  RequestException
import json

from config import *
from multiprocessing import Pool
#引入进程池，开启多进程

# client = pymongo.MongoClient(MONGO_URL)
client = pymongo.MongoClient(MONGO_URL, connect=False)
# 由于我们用了多进程，可能报警告，所以加一个, connect=False

db = client[MONGO_DB]
#声明mongodb对象

def get_page_index(offset,keyword):
    data={
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3
        #'cur_tab': 1,是综合页，检查很久才发现是错的，应该是3,“图集”
    }
    url = 'http://www.toutiao.com/search_content/?' + urlencode(data)
    #urlencode,把字典对象，转换成url的请求参数
    try:
        response = requests.get(url)
        if response.status_code==200:
            return response.text
        return None
        # print(url)
    except RequestException:
        print('请求索引也失败')
        return None

def parse_page_index(html):
# 解析内容
    data=json.loads(html)
#是json.loads()，不是json.load()
    if data and 'data' in data.keys():
        #加判断，保证data中有json属性
        #data.keys()反馈json所有的键名
        for item in data.get('data'):
            yield item.get('article_url')
        #yield 构造生成器


##获取详情页信息
def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code==200:
            return response.text
        return None
        print(url)
    except RequestException:
        print('请求详情页失败')
        return None

##解析url内容
def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    print('title:'+title)
    ### “时髦经典牛仔短裤，破一点更有潮流风，让奔三女性穿去街拍超有范”,格式不一样，不是通过gallery = 来获取
    images_pattern = re.compile('gallery = (.*?);', re.S)
    result = re.search(images_pattern, html)
    #有问题
    # print(result)
    if result and result is not None:
    # if result :
        print(result.group(1))
        data=json.loads(result.group(1))
        if data and 'sub_images' in data.keys():
            sub_images=data.get('sub_images')
            images=[item.get('url') for item in sub_images]
            #一句话完成列表形式构造，指每一个sub_images里面的item对象的URL属性
            for image in images: download_image(image,title)
            return {
                'title': title,
                'url': url,
                'images': images
            }
    else:
        print('格式不对，没有json格式')
        return False
        # return {
        #     'title': title,
        #     'url': '????????????',
        #     'images': '????????????'
        # }

def save_to_mongo(result):
##result字典的内容
    if db[MONGO_TABLE].insert(result):
        print('存储到MONGO成功',result)
        return True
    return False

# 下载图片
def download_image(url,title):
    print('正在下载：', url)
    try:
        response = requests.get(url)
        if response.status_code==200:
            # return response.text
            save_image(response.content,title)
            #response.content返回二进制
        return None
        print(url)
    except RequestException:
        print('请求图片失败')
        return None

def save_image(content,title):
    folder_path='c:\\toutiao\\'+title+'\\'
    # file_path = '{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    # file_path = '{0}/{1}/{2}.{3}'.format(os.getcwd(),title,md5(content).hexdigest(),'jpg')
    file_path = '{0}/{1}.{2}'.format(folder_path,md5(content).hexdigest(),'jpg')

    #md5,主要是防止下载失败后重新下载，产生重复图片。如果内容相同，md5就会相同
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print
        path + ' 创建成功'
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print
        path + ' 目录已存在'
        return False


# 定义要创建的目录
mkpath = "d:\\qttc\\web\\"
# 调用函数
mkdir(mkpath)

def main(offset):
# def main():
    # 引入多进程，才加到参数offset
    # html = get_page_index(0, '街拍')
    html = get_page_index(offset, KEYWORD)
    # print(html)
    for url in parse_page_index(html):
        html = get_page_detail(url)
        # print(html)
        if html:
            result=parse_page_detail(html,url)
            # print(result)
            # save_to_mongo(result)
            if result: save_to_mongo(result)


if __name__=='__main__':
    # main()
    groups = [x * 20 for x in range(GROUP_START,GROUP_END+1)]
    # 构造一个list
    pool = Pool()
    pool.map(main, groups)
