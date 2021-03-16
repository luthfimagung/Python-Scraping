from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from elasticsearch import Elasticsearch

PATH = "C:/Users/Luthfi M Agung/Downloads/Compressed/chromedriver_win32/chromedriver.exe"
es_client = Elasticsearch(["http://192.168.20.245:9200"])

drop_index = es_client.indices.delete(index='yt-trending', ignore=400)
create_index = es_client.indices.create(index='yt-trending', ignore=[400,404])

def main():
    driver = webdriver.Chrome(PATH)
    # options = webdriver.ChromeOptions()
    # options.headless = True
    #
    # options.binary_location = "C:/Users/Luthfi M Agung/AppData/Local/Google/Chrome/Application/chrome.exe"
    # driver = webdriver.Chrome(executable_path=PATH, options=options)
    driver.get("https://www.youtube.com/feed/trending")
    # all_videos = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='text-wrapper style-scope ytd-video-renderer']")))
    # video = all_videos.find_elements_by_id('dismissable')
    all_videos = WebDriverWait(driver, 10).until(lambda driver: driver.find_elements_by_css_selector("div[class='text-wrapper style-scope ytd-video-renderer']"))

    titles = []
    channels = []
    views = []
    links = []

    print("Kalemin.. Sabar..")

    id = 1
    for vid in all_videos:
        titles = vid.find_element_by_id("video-title").text
        channels = vid.find_element_by_id("text").text
        views = vid.find_element_by_css_selector("span[class='style-scope ytd-video-meta-block']").text
        links = vid.find_element_by_tag_name("a").get_attribute("href")
        print("Video title : " + titles)
        print("Channel : " + channels)
        print("Total Views : " + views)
        print("Video Link : " + links)
        print("-----------------------------------------------------------------------------------------------------")

        doc = {
            'trending' : id,
            'title' : titles,
            'channel' : channels,
            'views' : views,
            'link' : links
        }

        insert = es_client.index(index="yt-trending", body=doc)
        id += 1

    print("Beres")
    driver.quit()

main()