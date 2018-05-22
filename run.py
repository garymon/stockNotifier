# -*- coding: utf-8 -*-
import sys
import os
import telegram
import datetime
import requests
import util
import urllib
import konlpy
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join

reload(sys)
sys.setdefaultencoding('utf-8')


#============================ Stock Notifier ============================
def stock_notifier():
    url ="http://finance.daum.net/item/quote.daum?code=068270"

    response = urllib.urlopen(url)
    soup = BeautifulSoup(response, 'html.parser')

    price = soup.find('td', {'class': 'num quoteFst cUp'}).string
    print('celtrion : ' + price)

    #==send Message==
    send_telegram('celtrion : ' + price)


#==============================Real Estat News Notifier ==============================
#Today's real estate news. It's gonna be called in 11:30 every day.
def land_news_notifier():
    dt = datetime.datetime.now()
    today = dt.strftime("%Y%m%d")
    if not os.path.exists('articles/' + today):
        os.makedirs('articles/' + today)

    partialUrl = "http://land.naver.com/news/headline.nhn?bss_ymd=" + today
    response = urllib.urlopen(partialUrl)
    soup = BeautifulSoup(response, 'html.parser')
    links_with_text = []

    for a in soup.find_all('a', href=True):
        if a.text:
            links_with_text.append(a['href'])

    send_telegram("Hello. " + "Belows are " + today + "'s naver real estate news")

    for url in links_with_text:
        if "/news/newsRead.nhn?type=headline" in url:
            print('land.naver.com' + url)
            page = requests.get('http://land.naver.com' + url)
            soup = BeautifulSoup(page.content, 'html.parser')
            header = soup.find('div', {'class' : 'article_header'}).find('h3').get_text(strip=True)
            bodyContents = soup.find('div', {'id' : 'articleBody'}).get_text(strip=True)

            if check_new_article("(" + today +")" + header + ".txt") == True:
                send_telegram('land.naver.com' + url)
                f = open("articles/" + today + "/" + "(" + today + ")" + header + ".txt", 'w')
                f.write(bodyContents)
                f.close()
                print(header)
                print(bodyContents)


#==============================Finance News Notifier ==============================
#Today's finance news. It's gonna be called in 08:00 every morning. (Except to weekend)
#for i in range(0,10):
def finance_news_notifier():
    dt = datetime.datetime.now()
    today = dt.strftime("%Y%m%d")
    if not os.path.exists('articles/' + today):
        os.makedirs('articles/' + today)

    partialUrl = "http://finance.naver.com/news/mainnews.nhn?date=" + today + "&page=" + "1"
    print(partialUrl)
    response = urllib.urlopen(partialUrl)
    soup = BeautifulSoup(response, 'html.parser')
    links_with_text = []

    for a in soup.find_all('a', href=True):
        if a.text:
            links_with_text.append(a['href'])

    send_telegram("Hello. "+ "Belows are " + today + "'s naver finance news.")

    for url in links_with_text:
        if "/news/news_read.nhn?article_id=" in url and "type=&date" in url:
            print('finance.naver.com' + url)
            page = requests.get('http://finance.naver.com' + url)
            soup = BeautifulSoup(page.content, 'html.parser')
            header = soup.find('div', {'class' : 'article_header'}).find('h3').get_text(strip=True)
            bodyContents = soup.find('div', {'id' : 'content'}).get_text(strip=True)

            if check_new_article("(" + today +")" + header + ".txt") == True:
                send_telegram('finance.naver.com' + url)
                f = open("articles/" + today + "/" + "(" + today + ")" + header + ".txt", 'w')
                f.write(bodyContents)
                f.close()
                print(header)
                print(bodyContents)

#==============================Sender to telegram==============================
def send_telegram(msg):
    #bot = telegram.Bot(token = util.my_token)
    #bot.sendMessage(chat_id = util.my_chat_id, text = msg)
    print('success sending message')


#==============================check New?==============================
def check_new_article(headline):
    dt = datetime.datetime.now()
    today = dt.strftime("%Y%m%d")
    path = "articles/" + today
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for a in onlyfiles:
        if a == headline:
            return False
    return True

#==============================MAIN==============================
if __name__ == "__main__":
    stock_notifier()
    finance_news_notifier()
    land_news_notifier()
else:
    print('else')
