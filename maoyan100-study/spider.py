###猫眼受限制了，改成豆瓣
import requests
from requests.exceptions import RequestException
import json
import re
from multiprocessing import Pool
from pymongo import *

def get_one_page(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return None

# def parse_one_page(html):
#     pattern=re.compile('movie-list-item.*?movie-content.*?href="(.*?)".*?original="(.*?)"'
#                        +'movie-name-text.*?href="(.*?)".*?_blank">(.*?)</a>.*?"rank-num">(.*?)</span>'
#                        +'movie-misc">(.*?)</div>.*?rating_num">(.*?)</span>.*?comment-num">(.*?)</span>',re.S)
####豆瓣：   url='https://movie.douban.com/typerank?type_name=%E5%89%A7%E6%83%85&type=11&interval_id=100:90&action='

def parse_one_page(html):
    # compile_str='<li.*?number.*?<em>(.*?)</em>.*?mov_con.*?href="(.*?)".*?_blank">(.*?)</a>.*?导演'\
    #             +'.*?_blank">(.*?)</a>.*?主演.*?<a(.*?)</p>.*?类型.*?<span(.*?)</span>'\
    #             +'.*?class="mt3">(.*?)</p>.*?total">(\d+)</span>.*?total2">(.*?)</span>'\
    #             +'.*?<p>(.*?)</p>'
    compile_str='<li.*?number.*?<em>(.*?)</em>.*?mov_pic.*?src="(.*?)".*?mov_con.*?href="(.*?)".*?_blank">(.*?)</a>.*?<p>'\
                +'.*?_blank">(.*?)</a>.*?<p>.*?<a(.*?)</p>.*?<p>.*?<span(.*?)</span>'\
                +'.*?class="mt3">(.*?)</p>'
    pattern=re.compile(compile_str,re.S)
    items=re.findall(pattern,html)
    # print(items)
    for item in items:
        yield {
            'index':item[0],
            'pac':item[1],
            'url': item[2],
            'title': item[3],
            'director': item[4],
            # 'actor': re.sub('</a>\t\t|<a','',re.sub('class.*?"_blank">','',item[5])).strip(),
            'actor': re.sub('class.*?"_blank">|</a>\t\t|<a','',item[5]).strip(),
            'types': re.sub('class=.*?"_blank">|</a>|<em','',item[6]).strip(),
            'summary': item[7]
        }
def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()


def main(url1):
    url='http://www.mtime.com/top/movie/top100/'+str(url1)
    html=get_one_page(url)
    # parse_one_page(html)
    # for item in parse_one_page(html):
    #     print(item)
    item2=parse_one_page(html)
    for item in item2:
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    # index2=''
    # main(index2)
    # for i in range(2,11):
    #     index2='index-'+str(i)+'.html'
    #     main(index2)
    pool=Pool()
    pool.map(main,['index-'+str(i)+'.html' for i in range(2,11)])