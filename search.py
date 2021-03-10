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

keywords = {'valilik'}
SCROLL_PAUSE_TIME = 3

data = []
page = 1
total_page = 0
for keyword in keywords:
  count = 0
  wd.get("https://www.linkedin.com/search/results/content/?keywords=" + keyword + "&origin=FACETED_SEARCH&page=" + str(page) + "&sortBy=\"date_posted\"")
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

  result = soup.find("div", {"class": "search-marvel-srp"}).find("div").find("div")
  result = BeautifulSoup(str(result).replace('<br/>', '').replace(',', ' ').replace('\n', ''), 'html.parser').text
  result = result.split(" ")[0]

  if(int(result)%10 == 0):
    total_page = int(result)/10
  else:
    total_page = (int(result)/10) +1
  total_page = int(total_page)

  while(page <= total_page):
    wd.get("https://www.linkedin.com/search/results/content/?keywords=" + keyword + "&origin=FACETED_SEARCH&page=" + str(page) + "&sortBy=\"date_posted\"")
    time.sleep(SCROLL_PAUSE_TIME)
    last_height = wd.execute_script("return document.body.scrollHeight")

    while True:
      wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      #time.sleep(SCROLL_PAUSE_TIME)
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
          if(len(post_link)<1):
            post_link.append(a)

      #print(post_link)

      text = i.find("p", {"class": "entity-result__summary"})
      post1_text = BeautifulSoup(str(text).replace('\xa0', ' ').replace('…daha fazla gör', '').replace('None', '').replace('\n', ''),'html.parser').text
      post1_text = post1_text.rstrip()

      text2 = i.find("p", {"class": "entity-result__content-summary"})
      post2_text = BeautifulSoup(str(text2).replace('\xa0', ' ').replace('…daha fazla gör', '').replace('None', '').replace('\n', ''),'html.parser').text
      post2_text = post2_text.rstrip()
    
      h2 = i.find("h2", {"class": "entity-result__embedded-object-title t-14 mv1"})
      h2_text = BeautifulSoup(str(h2).replace('\xa0', ' ').replace('None', '').replace('\n', ''),'html.parser').text

      h3 = i.find("h3", {"class": "entity-result__embedded-object-sub-title t-12 t-black--light mv1"})
      h3_text = BeautifulSoup(str(h3).replace('\xa0', ' ').replace('…daha fazla gör', '').replace('None', '').replace('\n', ''),'html.parser').text
      h3_text = h3_text.split("•")[0]

      name = i.find("span", {"class": "entity-result__title-text t-16"})
      name_text = BeautifulSoup(str(name).replace('\n', '').replace('None', ''), 'html.parser').text
      name_text = name_text.split(" adlı")[0]
      length = len(name_text)%2
      if (length == 0):
        l = int(len(name_text)/2)
        name_text = name_text[l:]

      date = i.find("p", {"class": "entity-result__content-secondary-subtitle t-black--light t-12"})
      date_text = BeautifulSoup(str(date).replace(' •', '').replace('\n', ''), 'html.parser').text
      date_text = date_text.rstrip()
     
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

      if(len(post1_text)>0):
        if(post1_text == h2_text):
          post_text = post1_text + " " + h3_text

        else:
          post_text = post1_text + " " + h2_text + " " + h3_text

      else:
        if(len(post2_text)>0):
          post_text = post2_text

        else:
          post_text = h2_text + " " + h3_text

      post_text = post_text.strip()
      data.append([keyword, date_text, name_text, post_text, profile_photo, post_photo, post_link])

      count += 1
    print(keyword + ': ' + str(count))
    print(page)
    page += 1
    

  for i in data:
    print ("===========================================")
    print(i)
    print ("===========================================")
    #print(data)
wd.close()
