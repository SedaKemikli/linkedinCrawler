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

keywords = {'yasak'}
#milletvekili, belediye, mansur yavaş, ankara büyükşehir belediyesi, ekrem imamoğlu, istanbul büyükşehir belediyesi, tokat valiliği, çankaya belediyesi, emniyet genel müdürlüğü, mehmet aktaş, afyon valiliği, urfa büyükşehir belediyesi, ozan balcı, alper taşdelen, gökmen çiçek, zeynel abidin beyazgül'}
SCROLL_PAUSE_TIME = 3

data = {}
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
  soup = BeautifulSoup(wd.page_source, 'html.parser')
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
      time.sleep(SCROLL_PAUSE_TIME)
      new_height = wd.execute_script("return document.body.scrollHeight")
      if new_height == last_height:
        soup = BeautifulSoup(wd.page_source, 'html.parser')
        break
      last_height = new_height
    #soup = BeautifulSoup(wd.page_source, 'html.parser')
    #print(soup)

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
            post_link = post_link[0]

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

      title = i.find("div", {"class": "entity-result__primary-subtitle t-14 t-black"})
      title_text = BeautifulSoup(str(title).replace('\n', '').replace('None', ''), 'html.parser').text
      if(title_text.find('takipçi') != -1):
        follower_number = title_text.split(" takipçi")[0]
        if(follower_number.find('B') != -1 and follower_number.find('.') != -1 ):
          follower_number = BeautifulSoup(str(follower_number).replace('B', '00').replace('.', ''), 'html.parser').text
        else:
          follower_number = BeautifulSoup(str(follower_number).replace('B', '000'), 'html.parser').text
          #follower_number = int(follower_number)
        title_text =  ""
      else:
        follower_number= ""
      
      like_number = i.find("div", {"class": "entity-result__insights t-12"}).find("span")
      like_number = BeautifulSoup(str(like_number).replace('\n', '').replace('.','').replace('None', ''), 'html.parser').text
      print(like_number)

      comment_number = i.find("div", {"class": "entity-result__insights t-12"}).find("span", {"class": "v-align-middle"})
      comment_number = BeautifulSoup(str(comment_number).replace('\n', '').replace('.','').replace('None', ''), 'html.parser').text
      comment_number = comment_number.split(" Yorum")[0]

      date = i.find("p", {"class": "entity-result__content-secondary-subtitle t-black--light t-12"})
      date_text = BeautifulSoup(str(date).replace('\n', ''), 'html.parser').text
      date_text_result = ''

      if(date_text.count('•') > 1):
        date_text = date_text.split("•")[1]
        date_text = date_text.strip()
        #if(date_text.find('ay') > 1):

      else:
        date_text = date_text.split("•")[0]
        date_text = date_text.rstrip()

      if(date_text[1].isdigit()):
        date_text_result = date_find(date_text[2:], int(date_text[:2]))
      else:
        date_text_result = date_find(date_text[1:], int(date_text[:1]))
      date_text_result = date_text_result.strftime('%Y-%m-%d %H:%M:%S')
     
      src = []
      
      imgs = i.find_all("img", {"class": "ivm-view-attr__img--centered"})
     
      for j in imgs:
        src.append(j["src"])
      
      profile_photos = []
      post_photos = []
      profile_photo = ''


      if(len(src)>0):
        for j in src:
          if (j.find('profile') != -1) or (j.find('company') != -1):
            if(len(profile_photos)<1):
              profile_photos.append(j)
              profile_photo = profile_photos[0]

          elif (j.find('sync') != -1) or (j.find('feedshare') != -1):
            post_photos.append(j)
          else:
                if(len(profile_photo)<1):
                    profile_photo = ''

                elif(len(post_photos)<1):
                    post_photos = []
      else:
        profile_photo = ''
        post_photos = []

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
      if(date_text.find('ay') < 1) and (date_text.find('yıl') < 1) and (date_text.find('h') < 1):
        data={
                "link": post_link,
                "type": "post",
                "created_at": date_text_result,
                "text": post_text,

                "user":{
                "title": name_text,
                "description": title_text,
                "image_url": profile_photo,
                "counts": {
                    "followers": follower_number,
                }
                },
                "counts": {
                "likes": like_number,
                "comments": comment_number
                }
        }
        if len(post_photos) >0:
            data["entities"] = {
                "images": [{"image_url": post_photos[0] } ]
            } 
      sublist = list(chunks([data], 40))

      headers = {'X-Api-Key': 'MTYxODgxODcxNTk0OTUzNTY=',  'X-Secret-Key': '57e1a37b87391ffc.54ae83014fba874da0a97c8c8cccee20'}
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
