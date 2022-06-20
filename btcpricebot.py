from bs4 import BeautifulSoup
import requests
import time
import json
from selenium import webdriver
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
from datetime import datetime

def priceaggregate():
    r1 = requests.get('https://coinmarketcap.com/currencies/bitcoin/')
    soup = BeautifulSoup(r1.content, 'lxml')
    r2 = requests.get('https://www.coingecko.com/en/coins/bitcoin')
    soup2 = BeautifulSoup(r2.content, 'lxml')
    div2 = soup2.find('span', {'data-coin-symbol': 'btc'}).text[1:]
    div = soup.find_all('div', class_='priceValue')[0].text[1:]
    return (float(div.replace(',', '')) + float(div2.replace(',', ''))) / 2


while True:
    temptimeframe = input('Timeframe? (1min, 5min, 15min, 30min, 1hr, 2hr, 4hr, 1d, 1wk, 1mo)')
    timeframe = ''
    if temptimeframe == '1min':
        timeframe = '1 minute'
        break
    elif temptimeframe == '5min':
        timeframe = '5 minutes'
        break
    elif temptimeframe == '15min':
        timeframe = '15 minutes'
        break
    elif temptimeframe == '30min':
        timeframe = '30 minutes'
        break
    elif temptimeframe == '1hr':
        timeframe = '1 hour'
        break
    elif temptimeframe == '2hr':
        timeframe = '2 hours'
        break
    elif temptimeframe == '4hr':
        timeframe = '4 hours'
        break
    elif temptimeframe == '1d':
        timeframe = '1 day'
        break
    elif temptimeframe == '1wk':
        timeframe = '1 week'
        break
    elif temptimeframe == '1mo':
        timeframe = '1 month'
        break
    else:
        print('Invalid timeframe')
        continue

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.tradingview.com/symbols/BTCUSD/technicals/')

while True:
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    buttontexts = [button.text for button in buttons]

    index = buttontexts.index(timeframe)
    ActionChains(driver)\
        .click(buttons[index])\
        .perform()

    time.sleep(2)

    thistime = datetime.now()
    timestr = thistime.strftime('%Y-%m-%d %H:%M:%S')

    temp = {
        timestr: {
            'price': priceaggregate(),
            'oscillators': {},
            'movingaverages': {},
            'summary': {}
        }
    }

    tables = driver.find_elements(By.TAG_NAME, 'table')
    oscrows = tables[0].find_elements(By.TAG_NAME, 'tr')
    marows = tables[1].find_elements(By.TAG_NAME, 'tr')

    for i in range(len(oscrows)):
        if i == 0:
            pass
        else:
            tableelems = oscrows[i].find_elements(By.TAG_NAME, 'td')
            for x in range(len(tableelems)):
                name = tableelems[0].text
                temp[timestr]['oscillators'][name] = {}
                temp[timestr]['oscillators'][name]['value'] = tableelems[1].text
                temp[timestr]['oscillators'][name]['action'] = tableelems[2].text

    for i in range(len(marows)):
        if i == 0:
            pass
        else:
            tableelems = marows[i].find_elements(By.TAG_NAME, 'td')
            for x in range(len(tableelems)):
                name = tableelems[0].text
                temp[timestr]['movingaverages'][name] = {}
                temp[timestr]['movingaverages'][name]['value'] = tableelems[1].text
                temp[timestr]['movingaverages'][name]['action'] = tableelems[2].text

    speedometers = driver.find_elements(By.CLASS_NAME, 'speedometerSignal-RaUvtPLE')
    for i in range(len(speedometers)):
        if i == 0:
            temp[timestr]['oscillators']['estimate'] = speedometers[i].text
        elif i == 1:
            temp[timestr]['summary']['estimate'] = speedometers[i].text
        elif i == 2:
            temp[timestr]['movingaverages']['estimate'] = speedometers[i].text

    sell = 0
    buy = 0
    neutral = 0
    print(temp)
    for i in temp[timestr]['oscillators']:
        if i == 'estimate':
            pass
        else:
            if temp[timestr]['oscillators'][i]['action'] == 'Buy':
                buy += 1
            elif temp[timestr]['oscillators'][i]['action'] == 'Sell':
                sell += 1
            elif temp[timestr]['oscillators'][i]['action'] == 'Neutral':
                neutral += 1
    for i in temp[timestr]['movingaverages']:
        if i == 'estimate':
            pass
        else:
            if temp[timestr]['movingaverages'][i]['action'] == 'Buy':
                buy += 1
            elif temp[timestr]['movingaverages'][i]['action'] == 'Sell':
                sell += 1
            elif temp[timestr]['movingaverages'][i]['action'] == 'Neutral':
                neutral += 1

    temp[timestr]['summary']['buy'] = buy
    temp[timestr]['summary']['sell'] = sell
    temp[timestr]['summary']['neutral'] = neutral

    with open('data.json', 'r+') as f:
        file_data = json.load(f)
        file_data['data'].append(temp)
        f.seek(0)
        json.dump(file_data, f, indent=4)

    print('Saved Data')
    print('----------------------------------------------------')

    time.sleep(30)

    driver.refresh()
#    df = pd.DataFrame.from_dict(temp, orient='index')





