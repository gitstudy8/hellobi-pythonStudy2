from pyquery  import PyQuery as pq
import re
import requests
html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 " name='active2'><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
# print(doc('li'))
print (doc('li#name'))
# lis = doc('li').items()

# for li in lis:
#     print(li('li a').text())



#
# def get_page_index():
#     url = 'http://www.baidu.com/'
#     try:
#         response=requests.get(url)
#         if response.status_code==200:
#             return response.text
#         return None
#     except RequestException:
#         print('请求索引页出错！')
#         return None
#
# def main():
#     result=get_page_index()
#     # print(result)
#     doc=pq(result)
#     # item=doc('.list slide-item .section-box .section-item-box .class="section-title" ')
#     item=doc('#lh')
#     li=item.siblings()
#     print(li)
#
# if __name__ == '__main__':
#     main()
#
