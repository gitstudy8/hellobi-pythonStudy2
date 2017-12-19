from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver import ActionChains



browser=webdriver.Chrome()
# try:
#     browser.get('https://www.baidu.com')
#     input=browser.find_element_by_id('kw')
#     input.send_keys('大数据')
#     input.send_keys(Keys.ENTER)
#     # 键入回车
#     wait = WebDriverWait(browser, 10)
#     wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
#     # 等待，等id为content_left的元素倍加载出来,是双括号
#     print(browser.current_url)
#     print(browser.get_cookies())
#     # print(browser.page_source)
# finally:
#     browser.close()
#     # print('1')


# browser.get('https://www.taobao.com')
# input=browser.find_element_by_id('mq')
# input.send_keys('iphonex')
# time.sleep(5)
# input.clear()
# input.send_keys('ipad')
# # input.send_keys('iPad')
# # button = browser.find_element_by_class_name('btn-search')
# input.send_keys(Keys.ENTER)

#######将动作附加到动作链中串行执行ActionChains
# url='http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
# browser.get(url)
# browser.switch_to.frame('iframeResult')
# source=browser.find_element_by_css_selector('#draggable')
# target=browser.find_element_by_css_selector('#droppable')
# actions=ActionChains(browser)
# actions.drag_and_drop(source,target)
# actions.perform()

#####执行JavaScript
# ###进度条下拉
# browser.get('http://www.zhihu.com/explore')
# browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
# browser.execute_script('alert("To Bottom下拉到底部")')


browser.get('http://www.qq.com')
elem = browser.find_element_by_id("navMore")
print(elem)
browser.close()