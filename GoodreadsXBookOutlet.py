# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 17:02:46 2020

@author: Luiza
"""

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import json
import betterreads
from betterreads import client
import urllib.parse


def bookOutletHas(title, author):
    title = title.split(" (")[0]
    title_url = urllib.parse.quote_plus(title)
    url = 'https://bookoutlet.com/Store/Search?qf=All&q=' + title_url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.findAll('script')
    book_json = script[8].string
    book_json = book_json.split("products = ")[1]
    book_json = book_json.split(";")[0]
    correct_title = False;
    correct_author = True;
    book_json = book_json.lower()
    title = title.lower()
    
    if( title in book_json ):
        correct_title = True
    title_ind = book_json.find(title)
    
    if title_ind == -1:
        return [False,"not found"]
    
    auth_begin = book_json.lower().find("name", title_ind)
    auth_end = book_json.lower().find("id", title_ind)
    author_bo = book_json[auth_begin : auth_end ]
    
    if( author in author_bo ):
        correct_author = True
    author = author.lower().split()
    
    for a in author:
        if a not in author_bo:
            correct_author = False
            break
        
    if( correct_title & correct_author):
            return [True, url]
    return [False,"not found"]

#NEED TO ADD API KEY  TO USE THE GOODREADS API
#GO TO https://www.goodreads.com/api/keys
api_key = ""
api_secret = ""
user_id=""    #ID of user to check the shelf of, can be found in url of user profile
gc = client.GoodreadsClient(api_key, api_secret)
user = gc.user(user_id)
my_books = user.per_shelf_reviews(shelf_name = "to-read")
for review in my_books:
    temp_book = review.book
    title = temp_book["title"]
    author = temp_book["authors"]["author"]["name"]
    arr = bookOutletHas(title, author)
    if arr[0]:
        print("FOUND: " + title)
        print(arr[1])