from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests, time, sys
from webdriver_manager.chrome import ChromeDriverManager
import hashlib
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

username = 'example@hotmail.com'
password = '1111'

wd.get("https://www.linkedin.com/login/tr")
wd.find_element_by_id("username").send_keys(username)
wd.find_element_by_id("password").send_keys(password)
wd.find_element_by_class_name("from__button--floating").click()

keywords = {'ankara', 'istanbul', 'izmir'}
SCROLL_PAUSE_TIME = 3
data = {}

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def date_find(timetype, dif):
  today = datetime.now()
  difr = 0
  if(timetype == ' dakika '):
    difr = timedelta(minutes = dif)
  elif(timetype == ' saat '):
    difr = timedelta(hours = dif)
  elif(timetype == ' gün '):
    difr = timedelta(days = dif)
  elif(timetype == ' hafta '):
    difr = timedelta(weeks = dif)
  elif(timetype == ' ay '):
    dif = 4*dif
    difr = timedelta(weeks = dif)
  else:
    dif = 53*dif
    difr = timedelta(weeks = dif )
  return today - difr
  
for keyword in keywords:
  wd.get("https://www.linkedin.com/search/results/content/?keywords=" + keyword + "&origin=FACETED_SEARCH&sid=abc&sortBy=\"date_posted\"")
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
  posts = soup.findAll("div", {"class": "feed-shared-update-v2"})
 
  for i in posts:
    links = i.findAll("a", {"class": "app-aware-link"})
    href= []
    for a in links:
      if(len(href)<1):
        href.append(a["href"])
    href = href[0]

    if(i.find("div", {"class": "feed-shared-text"})!=None):
      text = i.find("div", {"class": "feed-shared-text"}).find("span", {"dir": "ltr"})
      post1_text = BeautifulSoup(str(text).replace('\xa0', ' ').replace('…daha fazla gör', '').replace('None', '').replace('\n', ''),'html.parser').text
      post1_text = post1_text.rstrip()

    h2 = i.find("h2", {"class": "feed-shared-article__title"})
    h2_text = BeautifulSoup(str(h2).replace('\xa0', ' ').replace('None', '').replace('\n', ''),'html.parser').text

    h3 = i.find("h3", {"class": "feed-shared-article__subtitle"})
    h3_text = BeautifulSoup(str(h3).replace('\xa0', ' ').replace('…daha fazla gör', '').replace('None', '').replace('\n', ''),'html.parser').text
    h3_text = h3_text.split("•")[0]

    name = i.find("span", {"class": "feed-shared-actor__name"})
    name_text = BeautifulSoup(str(name).replace('\n', '').replace('None', ''), 'html.parser').text

    title = i.find("span", {"class": "feed-shared-actor__description"})
    title_text = BeautifulSoup(str(title).replace('\n', '').replace('None', ''), 'html.parser').text

    if(title_text.find('takipçi') != -1):
      follower_number = title_text.split(" takipçi")[0].replace('.','')
      title_text = ""
    else:
      follower_number= ""
      title_text = title_text.strip()
    
    like_number = ""
    like_number = i.find("span", {"class": "social-details-social-counts__reactions-count"})
    like_number = BeautifulSoup(str(like_number).replace('\n', '').replace('.','').replace('None', ''), 'html.parser').text
    
    comment_number = ""
    comment_number = i.find("span", {"class": "social-details-social-counts__item-text--with-social-proof"})
    comment_number = BeautifulSoup(str(comment_number).replace('\n', '').replace('.','').replace('None', ''), 'html.parser').text
    comment_number = comment_number.split(" yorum")[0].strip()

    date = i.find("span", {"class": "feed-shared-actor__sub-description"})
    date_text = BeautifulSoup(str(date).replace('\n', '').replace(' önce', ''), 'html.parser').text
    date_text = date_text.split("•")[0]
    print(date_text+"zaman")

    if(date_text== 'şimdi '):
      date_text = "1 dakika "
      
    if(date_text[1].isdigit()):
      date_text_result = date_find(date_text[2:], int(date_text[:2]))
      date_text_result = date_text_result.strftime('%Y-%m-%d %H:%M:%S')
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

    if(post1_text != None):
      if(post1_text == h2_text):
        post_text = post1_text + " " + h3_text
      else:
        post_text = post1_text + " " + h2_text + " " + h3_text
      post_text = post_text.strip()
      
    id = hashlib.md5((href+date_text_result).encode('utf-8')).hexdigest()

    if((date_text.find('dakika') != -1) or (date_text.find('saat') != -1)):
      data={
            "id": id,
            "link": href,
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

      headers = {'X-Api-Key': 'api-key',  'X-Secret-Key': 'secret-key'}
      for i in sublist:
        r = requests.post('https://eas.etsetra.com/service/DataInsert', headers=headers, json={"data": i})
        print("=======================================================================")
        print(r.text)
        print("=======================================================================")
wd.close()
