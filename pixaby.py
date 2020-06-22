PATH = "C:\Program Files (x86)\chromedriver.exe"
from selenium import webdriver
import requests
import time
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re
from random import randint

# option is used to prevent websittes from detecting these scripts as bots

options = Options()
ua = UserAgent()
userAgent = ua.random
options.add_argument(f'user-agent={userAgent}')
driver = webdriver.Chrome(chrome_options=options, executable_path=PATH)

# items to scrape enables the python scripts to perform searches in pixaby website
itemsToScrape = 'house'

driver.get(f"https://pixabay.com/images/search/{itemsToScrape}")

time.sleep(10)
# the while loop with i represent how many pages do you want to visit if i is less than two then it will scrape only two pages
i = 0
while i < 56:
    # pagesource is use to get the present html page to scrape
    # pagesource source is a string so we cannot use selenium

    pageSource = driver.page_source

    # we are using beautifulsoup to get the the attributes of the img
    soup = BeautifulSoup(pageSource, 'html.parser')

    Images = soup.find_all('img')


    # Images returns  a list of html img element
    lenImages = int(len(Images))


    #  lenImages convert the len of Images to a integer that can be loop for accurate results
    print(Images)

    b = 36
    while b < lenImages:

        Imagessrc = Images[b].get('data-lazy')
        print(Imagessrc)

        r = requests.get(Imagessrc)
        # check if the image has an extension of jpg,png,gif,or jpeg  to store them with the png
        regex = r"\.jpeg|\.png|\.gif|\.jpg"

        imgName = re.search(regex, Imagessrc, re.MULTILINE).group()
        print(imgName)

        # download and store the image
        randnum = randint(1, 10000000000000000000000000000000)
        try:
            with open(f'image/{b}{randnum}{imgName}', 'wb') as file:
                file.write(r.content)
        except FileExistsError as e:
            print(e)
        b += 1

    next_page = driver.find_element_by_css_selector('#content > div > a')
    time.sleep(5)
    next_page.click()

    i += 1
