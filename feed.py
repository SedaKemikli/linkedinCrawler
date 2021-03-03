from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver', options=chrome_options)

username = 'yozg66@yandex.com'
password = '159263'

wd.get("https://www.linkedin.com/")
wd.find_element_by_id("session_key").send_keys(username)
wd.find_element_by_id("session_password").send_keys(password)
wd.find_element_by_class_name("sign-in-form__submit-button").click()

hashtags = {'kaymakam'}
SCROLL_PAUSE_TIME = 3

data = []

for hashtag in hashtags:
  count = 0
  wd.get("https://www.linkedin.com/feed/hashtag/?keywords=" + hashtag)
  time.sleep(SCROLL_PAUSE_TIME)
  last_height = wd.execute_script("return document.body.scrollHeight")

  while True:
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = wd.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
      soup = BeautifulSoup(wd.page_source, 'html.parser')
      break
    last_height = new_height

  posts = soup.findAll("div", {"class": "relative ember-view"})
  for i in posts:
    text = i.find("span", {"class": "break-words"})
    post_text = BeautifulSoup(str(text).replace('<br/>', ' <enter> ').replace(',', ' ').replace('\n', ' <enter> '),'html.parser').text

    name = i.find("span", {"class": "feed-shared-actor__name t-14 t-bold hoverable-link-text t-black"})
    name_text = BeautifulSoup(str(name).replace('<br/>', '').replace(',', ' ').replace('\n', ''), 'html.parser').text

    date = i.find("span", {"class": "feed-shared-actor__sub-description t-12 t-normal t-black--light"})
    date_text = BeautifulSoup(str(date).replace('<br/>', '').replace(',', ' ').replace('\n', ''), 'html.parser').text
    date_text = date_text[date_text.find('  ') + 2:]

    imgs = i.find_all("img", {"class": "ivm-view-attr__img--centered"})
    src = []
    for i in imgs:
      src.append(i["src"])
    #print(src)

    if (date_text == '      Öne çıkarılan içerik      ') or (date_text == 'one'):
      continue
    data.append([hashtag, date_text, name_text, post_text, src])

    count += 1
  print(hashtag + ': ' + str(count))

for i in data:
  print ("===========================================")
  print(i)
  print ("===========================================")
#print(data)
wd.close()
