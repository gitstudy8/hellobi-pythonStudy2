import pandas as pd

####################################################################
### 十分钟快速入门 Pandas
### http://codingpy.com/article/a-quick-intro-to-pandas/
### 英国降雨数据uk_rain_2014.csv
####################################################################


# Reading a csv into Pandas.
df = pd.read_csv('uk_rain_2014.csv', header=0)

# Getting first x rows.
# print(df.head(5))
# 我们只需要调用 head() 函数并且将想要查看的行数传入。
print('#######################################')
# Getting last x rows.
# print(df.tail(5))

# Changing column labels.改变列名称
df.columns = ['water_year','rain_octsep', 'outflow_octsep','rain_decfeb', 'outflow_decfeb', 'rain_junaug', 'outflow_junaug']
print(df.head(5))