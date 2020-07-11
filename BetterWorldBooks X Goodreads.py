# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 19:37:18 2020

@author: Luiza
"""
import requests
import urllib.request
from bs4 import BeautifulSoup
import json
import urllib.parse
from betterreads import client

def getISBN(title, author):
    title = title.split(" (")[0]
    title = urllib.parse.quote_plus(title)
    author = urllib.parse.quote_plus(author)
    url = "https://www.googleapis.com/books/v1/volumes?q=intitle:" + title + "+inauthor:" + author + "&key=AIzaSyA2yihooTCyRccN1Duxxcj3O5dz7aEB048"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)
    jsonx = json.loads( str(soup) )
    isbns = jsonx["items"][0]['volumeInfo']['industryIdentifiers']
    for isbn in isbns:
        if isbn['type'] == 'ISBN_10':
            print( isbn['identifier'] )
            

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True


url = "http://products.betterworldbooks.com/service.aspx?ItemId=1594634734"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'xml')
lowNew = soup.find('LowestNewPrice').find_all(text=True)[0]
lowUsed = soup.find('LowestUsedPrice').find_all(text=True)[0]
url = soup.find('DetailURLPage').find_all(text=True)[0]

user_id = "43329866"
api_key = "Eny1ro9b7mxhs8CuFj2o6w"
api_secret = "bQKcvwYsv0ceEBjk95guDtguTXRUSgBxGPBT0YtxD6U"

#url = "https://www.goodreads.com/search.xml?key=" + api_key + "&q=Ender%27s+Game"
url = "https://www.goodreads.com/shelf/list.xml?key=" + api_key + "&user_id=" + user_id
response = requests.get(url)
soup = BeautifulSoup(response.text, 'xml')
book_count = soup.find_all('user_shelf')[2].find('book_count').find_all(text=True)[0] #to-read
book_count = int(book_count)
all_books = []
for page in range(1,(book_count // 20)+2):
   url = "https://www.goodreads.com/review/list.xml?v=2&key=" + api_key + "&page=" + str(page) + "&id=" + user_id + "&shelf=to-read"
#    print(url)
   response = requests.get(url)
   soup = BeautifulSoup(response.text, 'xml')
   reviews = soup.find_all('review')
   for r in reviews:
       title = r.find('title').find_all(text=True)[0]
       author = r.find('name').find_all(text=True)[0]
       isbn = r.find('isbn')
       if '</isbn>' in isbn:
           isbn = isbn.find_all(text=True)[0]
           print(isbn)
       else:
           title = title.split(" (")[0]
           title = urllib.parse.quote_plus(title)
           author = urllib.parse.quote_plus(author)
           url = "https://www.googleapis.com/books/v1/volumes?q=intitle:" + title + "+inauthor:" + author + "&key=AIzaSyA2yihooTCyRccN1Duxxcj3O5dz7aEB048"
           #print(url)
           response = requests.get(url)
           soup = BeautifulSoup(response.text, 'html.parser')
           if validateJSON(str(soup)):
               jsonx = json.loads( str(soup) )
           else:
               continue
           if ('items' in jsonx):
               if 'industryIdentifiers' in jsonx["items"][0]['volumeInfo']:
                   isbns = jsonx["items"][0]['volumeInfo']['industryIdentifiers']
           else:
               continue
           for i in isbns:
               if i['type'] == 'ISBN_10':
                   isbn = i['identifier']
                   #print(isbn)
       url = "http://products.betterworldbooks.com/service.aspx?ItemId=" + isbn
       #print(url)
       response = requests.get(url)
       soup = BeautifulSoup(response.text, 'xml')
       if len( str(soup) ) > 100:
           lowNew = soup.find('LowestNewPrice').find_all(text=True)[0]
           lowUsed = soup.find('LowestUsedPrice').find_all(text=True)[0]
           url = soup.find('DetailURLPage').find_all(text=True)[0]
           print(title + " " + lowNew + " " + lowUsed + " " + url)
#        print(isbn)
#gr_books = user.per_shelf_reviews(shelf_name = "to-read")
#temp = gr_books[0]
        
