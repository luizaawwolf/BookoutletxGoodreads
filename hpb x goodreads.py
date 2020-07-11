# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 16:03:46 2020

@author: Luiza
"""

#from betterreads import client
#from betterreads.client import GoodreadsClient
#
#api_key = "Eny1ro9b7mxhs8CuFj2o6w"
#api_secret = "bQKcvwYsv0ceEBjk95guDtguTXRUSgBxGPBT0YtxD6U"
#gc = GoodreadsClient(api_key, api_secret)
#user = gc.user(user_id=12345)

#user_id = "43329866"
#api_key = "Eny1ro9b7mxhs8CuFj2o6w"
#api_secret = "bQKcvwYsv0ceEBjk95guDtguTXRUSgBxGPBT0YtxD6U"
#gc = client.GoodreadsClient(api_key, api_secret)
#user = gc.user(user_id)

# import HTMLSession from requests_html
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests

url = "https://www.hpb.com/products?utf8=%E2%9C%93#eyJmaWx0ZXJzIjp7InJhcmVGaW5kIjpmYWxzZSwibGFuZ3VhZ2UiOiJFTkcifSwidHlwZSI6bnVsbCwic29ydCI6bnVsbCwia2V5d29yZHMiOiJsYWR5IG1pZG5pZ2h0IGNhc3NhbmRyYSBjbGFyZSIsInNpemUiOjEwLCJmcm9tIjowfQ=="
#url = ""https://finance.yahoo.com/quote/NFLX/options?p=NFLX"" 
resp = requests.get(url)
html = resp.content
soup = BeautifulSoup(html)
#option_tags = soup.find_all("option")
 
## create an HTML Session object
#session = HTMLSession()
## Use the object above to connect to needed webpage
#resp = session.get(url)
## Run JavaScript code on webpage
#resp.html.render()
#















#WITH GECKODRIVER
# import libraries
#import urllib.request
#from bs4 import BeautifulSoup
#from selenium import webdriver
#import time
#import pandas as pd# specify the url
##urlpage = 'https://groceries.asda.com/search/yogurt' 
#urlpage = "https://www.hpb.com/products?utf8=%E2%9C%93#eyJmaWx0ZXJzIjp7InJhcmVGaW5kIjpmYWxzZSwibGFuZ3VhZ2UiOiJFTkcifSwidHlwZSI6bnVsbCwic29ydCI6bnVsbCwia2V5d29yZHMiOiJsYWR5IG1pZG5pZ2h0IGNhc3NhbmRyYSBjbGFyZSIsInNpemUiOjEwLCJmcm9tIjowfQ=="
#print(urlpage)
## run firefox webdriver from executable path of your choice
##driver = webdriver.Firefox(executable_path = "C:\\Users\\Luiza\\geckodriver-v0.26.0-win32\\geckodriver.exe")
### run firefox webdriver from executable path of your choice
###driver = webdriver.Firefox()
### get web page
##driver.get(urlpage)
### execute script to scroll down the page
##driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
### sleep for 30s
##time.sleep(30)
### driver.quit()
#
###WITH PHANTOMJS
#driver = webdriver.PhantomJS(executable_path = 'C:\\Users\\Luiza\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
## get web page
#driver.get(urlpage)
## execute script to scroll down the page
#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
## sleep for 30s
#time.sleep(30)
## driver.quit()
##results = driver.find_elements_by_xpath("//*[@class=' co-product-list__main-cntr']//*[@class=' co-item ']//*[@class='co-product']//*[@class='co-item__title-container']//*[@class='co-product__title']")
#results = driver.find_elements_by_xpath("//*[@class='search-result']")
#print('Number of results', len(results))
#
## create empty array to store data
#data = []
## loop over results
#for result in results:
#    print(result)
##    product_name = result.text
##    link = result.find_element_by_tag_name('a')
##    product_link = link.get_attribute("href")
##    # append dict to array
##    data.append({"product" : product_name, "link" : product_link})