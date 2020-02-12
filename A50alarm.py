import requests
import json           
import time
import pandas as pd
import config
#9:33~15:57
def getA50chart(x,y,z,w):
    custom_header = {
        'referer' : 'https://www.investing.com/charts/advinion.php?version=6.3.1.0&domain_ID=1&lang_ID=1&timezone_ID=8&pair_ID='+str(x)+'&interval=15M&user=204710788&majors='+str(y),
        'user-agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'  }
    url1="https://advcharts.investing.com/advinion2016/advanced-charts/1/1/8/GetRecentHistory?strSymbol="+str(x)+"&iTop=1500&strPriceType=bid&strFieldsMode=allFields&strUserID=204710788&strExtraData=lang_ID=1&strTimeFrame=1M"


    req = requests.get(url1, headers = custom_header)
    if req.status_code == requests.codes.ok:
        
        datalist = json.loads(req.text)
        data=datalist['data']
        data=pd.DataFrame(data)
        
    f=data.set_index('date')
    df=f[['open','high','low','close']]
    
    change=datalist['change']
    changePercent=datalist['changePercent']
    last=datalist['lastClose']
    df=df.tail(10)
    first_low=df['low'].iloc[0]
    first_high=df['high'].iloc[0]
    last_low=df['low'].iloc[9]
    last_high=df['high'].iloc[9]
    change_1=round((last_high/first_low - 1)*100,2)
    change_2=round((first_high/last_low - 1)*100,2)

    print(df)
    print(change_1,change_2)
    if abs(change_1) >= 1.00 :
        report='급변',change_1
    if abs(change_2) >= 1.00 :
        report='급변',change_2

    import telepot
    token = config.telegram_tocken
    mc = config.telegram_mc
    bot = telepot.Bot(token)

    bot.sendMessage(mc,report)

getA50chart('44486','new_touch_pairs_indices_futures','SGX China A50 Futures','A50futures.png')
