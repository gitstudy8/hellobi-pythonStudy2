########################################################################
####Python selenium —— 操作select标签的下拉选择框
####https://huilansame.github.io/huilansame.github.io/archivers/drop-down-select
########################################################################
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
import time

driver=webdriver.Chrome()
###针对于示例网站中的第一个select框：
# driver.get('http://sahitest.com/demo/selectTest.htm')
# s1=Select(driver.find_element_by_id('s1Id'))
# s1.select_by_index(1)# 选择第二项选项：o1
# time.sleep(5)
# s1.select_by_value('o1')
# time.sleep(5)
# s1.select_by_visible_text('o3')
# time.sleep(5)
# driver.close()
# driver.quit()

#####3.反选（deselect）
# deselect_by_index(index)
# deselect_by_value(value)
# deselect_by_visible_text(text)
# deselect_all()

#####4.选项（options）
# for select in s1.options:
#     print(select.text)

# s4=Select(driver.find_element_by_id('s4Id'))
# s4.select_by_index(1)
# s4.select_by_value('o3val')
# s4.select_by_visible_text('With spaces')##'With spaces'或者'    With spaces'效果一样
# s4.select_by_visible_text('    With nbsp')
# 空格' '，这种在以visible_text的方式选择时，不计空格，从第一个非空格字符开始
# 网页空格&nbsp;，对于这种以&nbsp;为空格的选项，在以visible_text的方式选择时，需要考虑前面的空格，每一个&nbsp;是一个空格
# for select in s4.all_selected_options:
#     print(select.text)

# ##3 想要查看选择框的默认值，或者我以及选中的值
# s2=Select(driver.find_element_by_id('s2Id'))
# print (s2.first_selected_option.text)
# s2.select_by_value('o2')
# print(s2.first_selected_option.text)

html='''
<html>
 <body>
  <form id="loginForm">
   <input name="username" type="text" />
   <input name="password" type="password" />
   <input name="continue" type="submit" value="Login" />
   <input name="continue" type="button" value="Clear" />
  </form>
</body>
<html>
'''
# print(html)
login_form=