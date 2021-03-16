from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from elasticsearch import Elasticsearch
import time

PATH = "C:/Users/Luthfi M Agung/Downloads/Compressed/chromedriver_win32/chromedriver.exe"
es_client = Elasticsearch(["http://192.168.20.245:9200"])

drop_index = es_client.indices.delete(index='twt-trending', ignore=400)
create_index = es_client.indices.create(index='twt-trending', ignore=[400,404])

def main():
    try:
        driver = webdriver.Chrome(PATH)
        driver.get("https://www.twitter.com/i/trends")

        wait = WebDriverWait(driver, 10)

        time.sleep(5)
        driver.execute_script("window.scrollTo(0,500);")
        time.sleep(5)

        print("Kalemin.. Sabar..")

        all_trends = wait.until(lambda driver: driver.find_elements_by_css_selector("div[class='css-1dbjc4n r-1igl3o0 r-qklmqi r-1adg3ll r-1ny4l3l']"))

        id = 1
        for trend in all_trends:
            wait_trend = WebDriverWait(trend, 10)
            topic = wait_trend.until(lambda trend: trend.find_element_by_css_selector("div[class='css-901oao r-1fmj7o5 r-1qd0xha r-a023e6 r-b88u0q r-ad9z0x r-bcqeeo r-vmopo1 r-qvutc0']")).text

            try:
                tweets = wait_trend.until(lambda trend: trend.find_element_by_css_selector(
                    "div[class='css-901oao r-9ilb82 r-1qd0xha r-n6v787 r-16dba41 r-1sf4r6n r-1g94qm0 r-bcqeeo r-qvutc0']")).text
            except:
                tweets = "Total tweets unknown."

            print(topic)
            print(tweets)
            print("-------------------")

            doc = {
                'trending': id,
                'topic': topic,
                'tweets': tweets
            }

            insert = es_client.index(index="twt-trending", body=doc)
            id += 1


    except:
        driver.quit()

    finally:
        print("Beres")
        driver.quit()

main()