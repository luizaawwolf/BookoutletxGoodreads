# -*- coding: utf-8 -*-
"""
Created on Sat May  2 16:30:18 2020

@author: Luiza
"""

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
from tkinter import *

#def libraryHas(title, author):
    #title = "A Curse So Dark And Lonely (3)"
title = "The Gilded Ones"
author = "Namina Forna"
title = title.split(" (")[0]
title_url = urllib.parse.quote_plus(title)
root = "https://bpl.overdrive.com" #https://ncdigital.overdrive.com"
url = root + '/search?query=' + title_url
print(url)
#url = 'https://bpl.overdrive.com/search?query=a+court+of+thorns+and+roses'
#print(url)
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
script = soup.findAll('script')
yikes_json = str( script[0].string )
yikes_json = yikes_json.split("window.OverDrive.mediaItems = ")
if len(yikes_json) < 2:
    print("no")
    quit
    #return [False, "broken"]
yikes_json = yikes_json[1]
yikes_json = yikes_json.split("window.OverDrive.thunderHost")[0]
if len(yikes_json) < 100:
    print("no")
    quit
    #return [False,"not found"]
yikes_json = yikes_json.split("}};")[0] + "}}"
books = json.loads(yikes_json)
my_books = []
if books:
    for book in books:
        correct_title = False;
        correct_author = True;
        book_info = books[book]
        od_title = book_info["title"].lower()
        od_author = book_info["firstCreatorName"].lower()
        available = book_info["isAvailable"]
        booktype = book_info["type"]["name"]
        print(booktype)
        if( od_title == title.lower() ):
            correct_title = True
            #print(correct_title)
            nms = author.lower().split()
            for nm in nms:
                #print(nm + " VS " + od_author)
                if nm not in od_author:
                    correct_author = False
        if correct_title and correct_author:
            #hasBook = True
            my_books += [[title,available,booktype]]
            #print("True")
    #return my_books
else:
    print("No")
    #return [False,"not found"]
    
#NEED TO ADD API KEY  TO USE THE GOODREADS API
#GO TO https://www.goodreads.com/api/keys
#api_key = "Eny1ro9b7mxhs8CuFj2o6w"
#api_secret = "bQKcvwYsv0ceEBjk95guDtguTXRUSgBxGPBT0YtxD6U"
##user_id="43329866"    #ID of user to check the shelf of, can be found in url of user profile
#gc = client.GoodreadsClient(api_key, api_secret)
#user_id = input("Enter Goodreads user ID: ")
#user = gc.user(user_id)
#my_books = user.per_shelf_reviews(shelf_name = "to-read")
#type_filter = input("Do you have a preference for type? (Audiobook/eBook/no): ")
#available_filter = input("Search only for available books? (t/f):" )
#print("Searching Boston Public Library for books on to-read shelf...")
#for review in my_books:
#    temp_book = review.book
#    title = temp_book["title"]
#    author = temp_book["authors"]["author"]["name"]
#    arr = libraryHas(title, author)
#    if arr and arr[0]:
#        for book in arr:
#            av = book[1]
#            if available_filter.lower() == "t" and not av:
#                #print("Not Available")
#                continue
#            typ = book[2]
#            if type_filter.lower() == "no":
#                print(book[0] + ", ", end = "")
#                if(book[1]):
#                    print("Available, " + book[2])
#                else:
#                    print("Not available, " + book[2])
#            else:
#                if typ.lower() == type_filter.lower():
#                    print(book[0])
#                
#    #if arr[0]:
    #    print("FOUND: " + title)
    #    print(arr[1])