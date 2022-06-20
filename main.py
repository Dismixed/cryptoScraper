from bs4 import BeautifulSoup
import requests
import json
from flask import Flask


app = Flask(__name__)


@app.get('/price/<symbol>')
def symbolprice(symbol):
    cmc = requests.get('https://coinmarketcap.com/')
    soup = BeautifulSoup(cmc.content, 'html5lib')
    for i in soup.find_all('tr'):
        templist = {
            'name': '',
            'symbol': '',
            'price': ''
        }
        text = i.contents[2]
        if i.contents[3].text[1:] == 'rice':
            pass
        else:
            print(i.contents[3])
            templist['price'] = i.contents[3].text[1:]

        for child in text.children:
            for child2 in child.contents:
                if child2.name == 'a':
                    for child3 in child2.contents:
                        templist['name'] = child3.contents[1].contents[0].text
                        templist['symbol'] = child3.contents[1].contents[1].text
                elif child2.name == 'span':
                    templist['name'] = child.contents[1].text
                    templist['symbol'] = child.contents[2].text

symbolprice('btc')

