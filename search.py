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

keywords = {'kaymakam'}
SCROLL_PAUSE_TIME = 3

data = []

for keyword in keywords:
  count = 0
  wd.get("https://www.linkedin.com/search/results/content/?keywords=" + keyword)
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

  posts = soup.findAll("li", {"class": "reusable-search__result-container artdeco-card search-results__hide-divider mb2"})
  for i in posts:

    links = i.find_all("a", {"class": "app-aware-link"})
    href= []
    post_link= []
    for a in links:
      href.append(a["href"])

    for a in href: 
      if (a.find('feed') != -1):
        post_link.append(a)

    print(post_link)

    text = i.find("p", {"class": "entity-result__summary entity-result__no-ellipsis mt3 t-14 t-black"})
    post_text = BeautifulSoup(str(text).replace('\xa0', ' ').replace('…daha fazla gör', '').replace(',', ' ').replace('\n', ' <enter> '),'html.parser').text

    text2 = i.find("p", {"class": "entity-result__content-summary entity-result__no-ellipsis t-14"})
    post2_text = BeautifulSoup(str(text2).replace('\xa0', ' ').replace('…daha fazla gör', '').replace(',', ' ').replace('\n', ' <enter> '),'html.parser').text

    h2 = i.find("h2", {"class": "entity-result__embedded-object-title t-14 mv1"})
    h2_text = BeautifulSoup(str(h2).replace('\xa0', ' ').replace('…daha fazla gör', '').replace(',', ' ').replace('\n', ' <enter> '),'html.parser').text

    h3 = i.find("h3", {"class": "entity-result__embedded-object-sub-title t-12 t-black--light mv1"})
    h3_text = BeautifulSoup(str(h3).replace('\xa0', ' ').replace('…daha fazla gör', '').replace(',', ' ').replace('\n', ' <enter> '),'html.parser').text
    #h3_text = h3_text[h3_text.find('•') + 2:]

    name = i.find("span", {"class": "entity-result__title-text t-16"}).find("span").find("span")
    name_text = BeautifulSoup(str(name).replace('<br/>', '').replace(',', ' ').replace('\n', ''), 'html.parser').text
    
    date = i.find("p", {"class": "entity-result__content-secondary-subtitle t-black--light t-12"})
    date_text = BeautifulSoup(str(date).replace(' •', '').replace(',', ' ').replace('\n', ''), 'html.parser').text
     
    imgs = i.find_all("img", {"class": "ivm-view-attr__img--centered"})
    src = []
    profile_photo = []
    post_photo = []
    for j in imgs:
      src.append(j["src"])

    for j in src:
      if (j.find('profile') != -1) or (j.find('company') != -1):
        if(len(profile_photo)<1):
          profile_photo.append(j)

      else:
        if(len(post_photo)<1):
          post_photo.append(j)

    #data.append([keyword, date_text, name_text, post_text, post2_text, h2_text, h3_text, profile_photo, post_photo])

    count += 1
  print(keyword + ': ' + str(count))

#for i in data:
  #print ("===========================================")
  #print(i)
  #print ("===========================================")
#print(data)
wd.close()
