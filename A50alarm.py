import requests
import time
import datetime as dt
from bs4 import BeautifulSoup
import pandas as pd


H=dt.timedelta(days=1)


now=dt.datetime.now()
now0=now-H
now1=now+H

t0=now0.strftime('%A %B %d %Y')
t=now.strftime('%A %B %d %Y')
nowt=now.strftime('%H:%M')
print(nowt)
t1=now1.strftime('%A %B %d %Y')

kt=now.strftime('%A %B %d')

timestamp=round(dt.datetime.timestamp(now))

url="https://tradingeconomics.com/calendar"
cookie='te-cal-countries=chn,usa; te-cal-importance=1; te-cal-range=3; TECalendarOffset=540; _ga=GA1.2.445467452.1577668410;  ASP.NET_SessionId=iuvqqldziyulh5kxaxt4cjn2; _gid=GA1.2.313629741.'+str(timestamp)+'; TEServer=TEIIS; _gat=1'
cookie=cookie.encode('utf-8')
custom_header = {
    'referer' : 'https://tradingeconomics.com/calendar',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'cookie' : cookie}
req = requests.get(url,headers = custom_header)
soup = BeautifulSoup(req.text, 'html5lib')
data=soup.find('table',{'id':'calendar'})

date=data.find_all('thead',{'class':'table-header'})
sort=soup.select('#calendar > tbody')

df=pd.read_csv('category_list.txt',header=None)

result_list=[]
for i in range(len(date)):
    date1=date[i].select('th')[0].text.strip()

    if date1==t:
            
        result_list1=[]
        for j in range(len(df)):
            Country=df[0].values.tolist()
            Category=df[1].values.tolist()
            sort1=sort[i].find('tr',{'data-country':Country[j],'data-event':Category[j]})
            if sort1 != None:
                time=sort1.select('span')[0].text.strip()
                time=dt.datetime.strptime(str(time), '%I:%M %p')
                time=time.strftime('%H:%M')
                country=sort1.find('td',{'class':'calendar-iso'}).text.strip()
                title=sort1.select('td')[4].text.strip()
                title=title.split('\n')[0].strip()
                previous=sort1.find('span',{'id':'previous'}).text.strip()
                consensus=sort1.find('a',{'id':'consensus'})
                actual=sort1.find('span',{'id':'actual'}).text.strip()
                if actual=='':
                    if nowt>time:
                        if consensus != None :
                            consensus=consensus.text.strip()
                            result=str(time)+' '+str(country)+' '+str(title)+\
                                  '\n(Actual: '+str(actual)+\
                                  ', Consensus: '+str(consensus)+\
                                  ', Previous: '+str(previous)+\
                                  ')'
                        else:
                            result=str(time)+' '+str(country)+' '+str(title)
                        result_list1.append(result)
                        result_listt1=sorted(result_list1,key=lambda x:x[:5])

        result_list.append(result_list1)
rl=[]
for r in result_list:
    result_list = "\n\n".join(r[0:])
    rl.append(result_list)
result_list= "\n\n".join(rl[0:])
print(result_list)


import telepot

token = "827312654:AAFnFx7a9G5W4j7TwJJ50HMoSaaCEjfLu0A"
mc = "-1001227507866"
mc = "694014464"
bot = telepot.Bot(token)

#bot.sendMessage(mc,result_list)
