# -*- coding: utf-8 -*-
import sys
import os
import telegram
import datetime
import requests
import util
from six.moves import urllib
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

#============================ Stock Notifier ============================
url ="http://finance.daum.net/item/quote.daum?code=068270"

response = urllib.request.urlopen(url)
bot = telegram.Bot(token = util.my_token)
updates = bot.getUpdates()
for u in updates :
    print(u.message)

soup = BeautifulSoup(response, 'html.parser')

price = soup.find('td', {'class': 'num quoteFst cUp'}).string

print('celtrion : ' + price)

#send Message
#bot.sendMessage(chat_id = '@peries_bot', text='celtrion : ' + price)




dt = datetime.datetime.now()
today = dt.strftime("%Y%m%d")
if not os.path.exists(today):
    os.makedirs(today)

#==============================Real Estat News Notifier ==============================

#Today's real estate news. It gonna be called in 11:30 every day.

partialUrl = "http://land.naver.com/news/headline.nhn?bss_ymd=" + today
response = urllib.request.urlopen(partialUrl)
soup = BeautifulSoup(response, 'html.parser')
links_with_text = []

for a in soup.find_all('a', href=True):
    if a.text:
        links_with_text.append(a['href'])

#bot.sendMessage(chat_id=my_chat_id, text="Hello. " + "This is " + today + "'s naver real estate news")

for url in links_with_text:
    if "/news/newsRead.nhn?type=headline" in url:
        print('land.naver.com' + url)
        page = requests.get('http://land.naver.com' + url)
        soup = BeautifulSoup(page.content, 'html.parser')
        header = soup.find('div', {'class' : 'article_header'}).find('h3').get_text(strip=True)
        print(header)
        bodyContents = soup.find('div', {'id' : 'articleBody'}).get_text(strip=True)
        print(bodyContents)
        f = open(today + "/" + "(" + today + ")" + header + ".txt", 'w')
        f.write(bodyContents)
        f.close()
        #bot.sendMessage(chat_id=my_chat_id, text='land.naver.com' + a)



#==============================Finance News Notifier ==============================

#Today's finance news. It gonna be called in 08:00 every morning. (Except to weekend)

#for i in range(0,10):
partialUrl = "http://finance.naver.com/news/mainnews.nhn?date=" + today + "&page=" + "1"
print(partialUrl)
response = urllib.request.urlopen(partialUrl)
soup = BeautifulSoup(response, 'html.parser')
links_with_text = []

for a in soup.find_all('a', href=True):
    if a.text:
        links_with_text.append(a['href'])

#bot.sendMessage(chat_id=my_chat_id, text="Hello. "+ "This is " + today + "'s naver finance news.")

for url in links_with_text:
    if "/news/news_read.nhn?article_id=" in url and "type=&date" in url:
        print('finance.naver.com' + url)
        page = requests.get('http://finance.naver.com' + url)
        soup = BeautifulSoup(page.content, 'html.parser')
        header = soup.find('div', {'class' : 'article_header'}).find('h3').get_text(strip=True)
        print(header)
        bodyContents = soup.find('div', {'id' : 'content'}).get_text(strip=True)
        print(bodyContents)
        f = open(today + "/" + "(" + today + ")" + header + ".txt", 'w')
        f.write(bodyContents)
        f.close()
        #bot.sendMessage(chat_id=my_chat_id, text='finance.naver.com' + url)