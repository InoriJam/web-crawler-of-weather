#coding=utf-8
import requests
import re
import csv
import os
import time

#输入城市
print("请输入城市名称(汉语拼音小写)")
city=input()
print("请输入城市中文名称")
chsname=input()
#获取当前年月日
timearr=re.split('-',time.strftime('%Y-%m-%d',time.localtime(time.time())))
#设置起始年月
year=2011
month=1
#建立数据存放路径
os.mkdir("抓取数据")
#创建表头list
CsvHead=['日期','最高气温','最低气温','白天天气','夜间天气','风向','风力']
#新建Session
session_requests=requests.session()
#遍历每年每月的数据
while(year<=int(timearr[0])):
    while(month<=12):
        try:
            #拼接url
            if(year<int(timearr[0])):
                url="http://15tianqi.cn/"+str(year)+city+str(month)+"yuetianqi/"
            else:
                url="http://15tianqi.cn/"+city+str(month)+"yuetianqi/"
            #获取请求url后返回的对象
            res=session_requests.get(url)
            #设置页面编码
            res.encoding='utf-8'
            #正则匹配
            HtmlInfo=r'''<tr><td><a href="/(.*?)/" title="(.*?)" target="_blank">(.*?)</a></td><td>(.*?)℃</td><td>(.*?)℃</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td class="rnoborder">(.*?)</td></tr>'''
            match=re.findall(HtmlInfo,res.text)
            #建立文件
            file=open('抓取数据\\'+chsname+str(year)+'年第'+str(month)+'月天气'+'.csv','w',newline='')
            data=csv.writer(file)
            #写入CSV表头
            data.writerow(CsvHead)
            #遍历匹配结果并筛选
            for ele in match:
                data.writerow(ele[2:])
            #关闭文件
            file.close()
            #准备抓取下一月数据
            month+=1
        except:
            #异常处理：直接跳转到下一月
            month+=1
        #当遍历到当前月份上一月时结束
        if(year==int(timearr[0])) and (month==int(timearr[1])):
            break
    #重置起始月份和增加年份
    year+=1
    month=1
#完成
print("DONE!")

