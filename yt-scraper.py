from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pymongo
from pymongo import MongoClient

cluster = MongoClient('127.0.0.1', 27017)
db = cluster["scraping"]
collection = db["youtube"]
PATH = "C:/Users/Luthfi M Agung/Downloads/Compressed/chromedriver_win32/chromedriver.exe"

def main():
    driver = webdriver.Chrome(PATH)
    driver.get('https://www.youtube.com/feed/trending')
    content = driver.page_source.encode('utf-8').strip()
    titles = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#video-title")))
    # descriptions = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#description-text")))
    # content = titles + descriptions

    for title in titles:
        # print(title.text)
        post = {
            'video title': title.text
        }
        collection.insert_one(post)

    driver.quit()

main()