###  可以运行，可以翻页，没有获取详细信息
import re
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
# 后面很多都会用得到，所以直接定义为一个变量
#建搜索方法
def search():
    try:
        browser.get('https://world.taobao.com')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
            # 怎么是双括号(())
        )
        ###  EC表示只要加载出来就好
        submit= wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button"))
        )
        # element_to_be_clickable，是等到可以点击的
        # 在浏览器调试中，选择按钮，选中代码--右键--copy--CSS_SELECTOR
        #加载需要时间，增加一个加载时候成功的方法
        input.send_keys('美食')
        submit.click()
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#list-page > div > div > span:nth-child(9)"))
        )
        # 等待页面(总页数)加载完成
        return total.text
    except TimeoutException:
        return search()
def next_page(page_number):
    print('正在翻页', page_number)
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#list-page > div > div > input"))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#list-page > div > div > button"))
        )

        browser.execute_script("window.scrollBy(0,200)", "")  # 向下滚动200px
        browser.execute_script("window.scrollBy(0,document.body.scrollHeight)", "")  # 向下滚动到页面底部
        # 添加滚动后，可以运行了
        time.sleep(2)
        input.clear()
        input.send_keys(page_number)
        submit.click()
        '''
        selenium.common.exceptions.WebDriverException: Message: unknown error: Element <button class="submit" type="button">...</button> is not clickable at point (763, 565). Other element would receive the click: <div class="pic">...</div>
        这三个异常都与Chrome的运行速度以及WebDriverWait的可靠性有一定关系。因此，我们可以稍显“粗暴”的让webdriver休眠一段时间来slow down测试代码的执行速度，强制driver等待一个固定的时间来让元素加载完成。
        time.sleep(2)
        3.不在当前视图范围内的元素的操作
        当我们使用Firefox webdriver来测试某个页面的时候，如果我们选取了某个页面元素来对其进行操作，但是这个元素不在当前浏览器显示的视图范围内，Firefox webdriver的做法是自动的将视图调整到该元素显示的区域，然后对这个元素进行操作。也就是说driver自己完成了页面的scroll down or up的操作。
        但是在Chrome webdriver中，如果待操作元素不在视图显示范围内，则会抛出Element is not clickable at point异常。或是如果设置了WebDriverWait并且它正常工作的话会抛出Timeout异常。
        http://www.cnblogs.com/harolei/p/3466284.html
        '''
        '''
        因此，在使用Chrome wbedriver的时候，我们要更加小心，对于需要滚动页面才能显示在视图中的元素，我们需要添加代码使页面滚动至元素显示的范围，然后再对该元素进行操作。使页面滚动的方法是：
        driver.execute_script("window.scrollBy(0,200)","")  #向下滚动200px
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight)","")  #向下滚动到页面底部
        '''
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#list-page > div > div > span.active'), str(page_number)))
        # 判定页码是否高亮度，是否str(page_number)一致
    except TimeoutException:
        next_page(page_number)
        # 重新执行一下这个请求，递归调用

#无 def get_products():


def main():
    total = search()
    total=int(re.compile('(\d+)').search(total).group(1))
    #提取页面数字
    # print(total)
    for i in range(2, total+1):
        next_page(i)
        # print(i)

if __name__ == '__main__':
    main()
