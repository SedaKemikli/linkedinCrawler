from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
import requests, json, time, sys
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
page = 1
total_page = 0

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def date_find(timetype, dif):
  today = datetime.now()
  difr = 0
  if(timetype == 'a'):
    difr = timedelta(minutes = dif)
  elif(timetype == 's'):
    difr = timedelta(hours = dif)
  elif(timetype == 'g'):
    difr = timedelta(days = dif)
  elif(timetype == 'h'):
    difr = timedelta(weeks = dif)
  elif(timetype == 'ay'):
    dif = 4*dif
    difr = timedelta(weeks = dif)
  else:
    dif = 53*dif
    difr = timedelta(weeks = dif )
  return today - difr

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
    #date_text = date_text[date_text.find('  ') + :]
    
    if (date_text == '      Öne çıkarılan içerik      ') or (date_text == 'one'):
      continue

    #wd.find_element_by_css_selector("#"+i["id"]+" "+".feed-shared-control-menu__trigger").click()

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
      #print(src)


    
    #data.append([hashtag, date_text, name_text, post_text, profile_photo, post_photo])
    data={
          "link": ,
          "type": "post",
          "created_at": ,
          "text": post_text,

          "user":{
            "title": name_text,
            "description": ,
            "image_url": profile_photo,
            "counts": {
              "followers": ,
            }
          },

          "entities": {
              "images": [
                {"image_url": post_photo} 
              ]
          },

          "counts": {
            "likes": ,
            "comments": 
          }
    }
    sublist = list(chunks([data], 40))

    headers = {'X-Api-Key': 'MTYxNjAwMzE1NTY3MzcwMjQ=',  'X-Secret-Key': 'a351852c1ea3fa9f.6a02b6a8fe9b6000354bb346dd01165e'}
    for i in sublist:
      r = requests.post('https://eas.etsetra.com/service/DataInsert', headers=headers, json={"data": i})
      # print("=======================================================================")
      # print(i)
      print("=======================================================================")
      print(r.text)
      print("=======================================================================")
      #data.append([keyword, date_text_result, name_text, title_text, profile_photo, follower_number, post_text, post_photo, post_link])

    count += 1
    #print(keyword + ': ' + str(count))
    #print(page)
  page += 1
    

    #print(data)
wd.close()
