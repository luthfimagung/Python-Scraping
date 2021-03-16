from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from elasticsearch import Elasticsearch
from datetime import datetime
import time
import hashlib
import pytz

PATH = "C:/Users/Luthfi M Agung/Downloads/Compressed/chromedriver_win32 (89)/chromedriver.exe"
es_client = Elasticsearch(["http://192.168.20.245:9200"])

mapping = {
    "mappings": {
        "properties": {
            "input_date": {
                "type": "date"
            },
            "content_id": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 1024
                    }
                }
            },
            "image_link": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 1024
                    }
                }
            },
            "image_info": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 1024
                    }
                }
            },
            "image_source": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 1024
                    }
                }
            }
        }
    }
}

drop_index = es_client.indices.delete(index='ig-hashtag', ignore=400)
create_index = es_client.indices.create(index='ig-hashtag', body=mapping, ignore=[400,404])

def main():
    driver = webdriver.Chrome(PATH)
    # driver.delete_all_cookies()
    # time.sleep(7)

    driver.get("https://www.instagram.com/explore/tags/cats/")
    # driver.get("https://www.instagram.com/explore/tags/artoftheday/")

    wait = WebDriverWait(driver, 10)

    # time.sleep(5)
    # driver.execute_script("window.scrollTo(0,500);")
    # time.sleep(5)

    # all_contents = wait.until(lambda driver: driver.find_element_by_css_selector("article[class='KC1QD']"))
    # all_images = wait.until(lambda all_contents: all_contents.find_elements_by_css_selector("div[class='v1Nh3 kIKUG  _bz0w']"))
    all_images = wait.until(lambda imagedriver: driver.find_elements_by_css_selector("div[class='v1Nh3 kIKUG  _bz0w']"))

    for image in all_images:

        utc = pytz.timezone("Asia/Jakarta")
        now = datetime.now()
        tz_aware_dt = utc.localize(now)
        date_string = tz_aware_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        wait_image = WebDriverWait(image, 10)

        img_source = wait_image.until(lambda image: image.find_element_by_tag_name("img").get_attribute("src"))
        img_info = wait_image.until(lambda image: image.find_element_by_tag_name("img").get_attribute("alt"))
        img_link = wait_image.until(lambda image: image.find_element_by_tag_name("a").get_attribute("href"))

        img_link_str = str(img_link)
        img_link_hash = hashlib.md5(img_link_str.encode())
        hash_link_md5 = img_link_hash.hexdigest()

        print("Input date: " + date_string)
        print("Content Id: " + hash_link_md5)
        print("Content Link: " + img_link)
        print("Content Info: " + img_info)
        print("Content Source: " + img_source)
        print("-------------------------------------------")

        doc = {
            'input_date': date_string,
            'content_id': hash_link_md5,
            'image_link': img_link,
            'image_info': img_info,
            'image_source': img_source
        }

        es_client.index(index="ig-hashtag", body=doc, id=hash_link_md5)

    driver.quit()

main()