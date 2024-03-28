from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
from datetime import datetime

news_set = set()

while True:
    website = "https://finviz.com/"
    path = "../chromedriver-win64/chromedriver.exe"
    #Introduce the service 
    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service)

    driver.get(website)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'News'))
    )

    href = driver.find_element(By.LINK_TEXT, 'News')

    href_value = href.get_attribute('href')
    # print(href_value)
    driver.get(href_value)

    WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'news_link-cell'))
    )

    news_array = driver.find_elements(By.CLASS_NAME, 'news_link-cell')

    def sendMessage(news, link):
        bot_id = "7032862501:AAGrZ21Pu1aa5x6EC75yVt5ZIepWhet0Pck"
        chat_id = "-1002127524714"
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        message = date_time + "\n" + news + "\n" + link
        print(message)

        url = f"https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text={message}"
        return requests.get(url).json()


    for news in news_array:
    
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "a"))
        )
        href = news.find_element(By.TAG_NAME, "a")
        ref_link = href.get_attribute('href')
        if "fed" in news.text.lower() or "rate" in news.text.lower():
            if ref_link not in news_set:
                sendMessage(news.text, ref_link)
                news_set.add(ref_link)
        
    driver.implicitly_wait(100000)

    driver.quit()

    time.sleep(60)
