# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 17:02:46 2020

@author: Luiza
"""

import requests
import urllib.request
from bs4 import BeautifulSoup
from betterreads import client
import urllib.parse


def bookOutletHas(title, author):
    title = title.split(" (")[0]
    title_url = urllib.parse.quote_plus(title)
    url = 'https://bookoutlet.com/Store/Search?qf=All&q=' + title_url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.findAll('div','grid-item')
    search_results = []
    correct_title = False;
    correct_author = True;
    for a in items:
        ret_author = a.find('p','author').find_all(text=True)[0]
        ret_title = a.find('a','line-clamp-2').find_all(text=True)[0]
        if author.lower() in ret_author.lower():
            print("Hey")
        if author.lower() in ret_author.lower():
            correct_author = True
        if title.lower() in ret_title.lower():
            correct_title = True
        else:
            for name in author:
                if name not in ret_author:
                    correct_author = False
                    continue
        if( correct_title and correct_author):
            link_url = "https://bookoutlet.com" + a.find_all('a',href=True)[0]['href']
            image_url = "https:" + a.find_all('img')[0]['src']
            search_results += [[author,title,link_url,image_url]]
    return search_results

#NEED TO ADD API KEY  TO USE THE GOODREADS API
#GO TO https://www.goodreads.com/api/keys
api_key = "Eny1ro9b7mxhs8CuFj2o6w"
api_secret = "bQKcvwYsv0ceEBjk95guDtguTXRUSgBxGPBT0YtxD6U"
user_id="43329866"    #ID of user to check the shelf of, can be found in url of user profile
gc = client.GoodreadsClient(api_key, api_secret)
#user_id = input("Enter your user ID: ")
user = gc.user(user_id)
my_books = user.per_shelf_reviews(shelf_name = "currently-reading")
for review in my_books:
    temp_book = review.book
    title = temp_book["title"]
    author = temp_book["authors"]["author"]["name"]
    results = bookOutletHas(title, author)
    if results:
        print(results)