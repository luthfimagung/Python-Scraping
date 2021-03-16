import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient

cluster = MongoClient('127.0.0.1', 27017)
db = cluster["scraping"]
collection = db["instagram"]
PATH = "C:/Users/Luthfi M Agung/Downloads/Compressed/chromedriver_win32/chromedriver.exe"

urls = [
    'detikcom',
    'jokowi',
    'jktinfo',
]

def main():
    driver = webdriver.Chrome(PATH)
    for url in urls:
        driver.get('https://www.instagram.com/{}/'.format(url))
        content = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, 'lxml')
        content = soup.findAll('img', class_='FFVAD')

        # img_text = []
        # src = []
        for c in content:
            img_info = c.get('alt')
            src = c.get('src')
            post = {
                'publisher':'@'+url,
                'image_src':src,
                'image_info':img_info,
            }
            collection.insert_one(post)

main()