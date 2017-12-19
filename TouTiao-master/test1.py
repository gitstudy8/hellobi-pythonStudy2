import requests
import re
from urllib.parse import urlencode
from requests.exceptions import RequestException
import json
from bs4 import BeautifulSoup
import pymongo

MONGO_URL = 'localhost'
MONGO_DB = 'toutiao'
MONGO_TABLE = 'test1'

client = pymongo.MongoClient('localhost')
db = client['trip']


# client=pymongo.MongoClient(MONGO_URL)
client=pymongo.MongoClient(MONGO_URL,connect=False)
db=client[MONGO_DB]

def get_result(offset,keyword):
    data={
        'offset': offset,
        'keyword': keyword
    }

def main():
    data={
        'id': 1,
        'keyword': 'kw'
    }

    # for i in range(10):
    #     data['id']=str(i)
    #     print(data)
    #     db[MONGO_TABLE].insert(data)
    #     print('存储到MongoDB成功', data)
    db[MONGO_TABLE].insert(data)
    # for i in range(10):
    #     if db[MONGO_TABLE].insert(result):
    #         print(i)
    #         print('存储到MongoDB成功', result)
    #         return True
    #     return False

if __name__ == '__main__':
    main()
