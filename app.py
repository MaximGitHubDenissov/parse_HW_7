from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'

link = 'https://finance.yahoo.com/most-active/'

chrome_option = Options()
chrome_option.add_argument(f"user_agent = {user_agent}")
driver = webdriver.Chrome(options=chrome_option)

driver.get(link)

WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))
size_length = driver.execute_script('return document.documentElement.scrollHeight')
while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1)
        size_new = driver.execute_script('return document.documentElement.scrollHeight')
        if size_new == size_length:
            break
        else:
            size_length = size_new
print(size_length)

symbols = driver.find_elements(By.XPATH, '//*[@id="scr-res-table"]/div/table/tbody/tr/td/a')
names = driver.find_elements(By.XPATH, '//*[@id="scr-res-table"]/div[1]/table/tbody/tr/td[2]') 
prices = driver.find_elements(By.XPATH, '//*[@id="scr-res-table"]/div[1]/table/tbody/tr/td[3]/fin-streamer')
changes = driver.find_elements(By.XPATH, '//*[@id="scr-res-table"]/div[1]/table/tbody/tr/td[5]/fin-streamer/span')

data = []
for i in range(len(symbols)):
     item = {'symbol': symbols[i].text,
             'name': names[i].text,
             'price': prices[i].text,
             'change': changes[i].text}
     data.append(item)

with open ('results.json', 'w', encoding='UTF-8') as file:
     json.dump(data, file, ensure_ascii=False, indent=4)

