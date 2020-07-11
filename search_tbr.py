# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 21:50:53 2020

@author: Luiza
"""

#by pages
#if part of series
#place to get book: library, amazon, kindle unlimited, etc
#genre
#average review

from betterreads import client
import requests
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse
import json
import itertools

class Book():
    def __init__(self, title, author, pgcount, genres, series):
        self.title = title
        self.author = author
        self.pgcount = pgcount
        self.genres = genres
        self.series=series
        #self.genre_tags
        #self.ave_review
        #self.series bool

def libraryHas(title, author, root, only_available=False, ebooks=True, audiobooks=True):
    title = title.split(" (")[0]
    title_url = urllib.parse.quote_plus(title)
    #root = "https://bpl.overdrive.com/"
    url = root + "search?query=" + title_url
    #url = 'https://bpl.overdrive.com/search?query=a+court+of+thorns+and+roses'
    #print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.findAll('script')
    yikes_json = str( script[0].string )
    yikes_json = yikes_json.split("window.OverDrive.mediaItems = ")
    my_books = []
    if len(yikes_json) < 2:
        my_books += ["ERROR"]
        return my_books
    yikes_json = yikes_json[1]
    yikes_json = yikes_json.split("window.OverDrive.thunderHost")[0]
    if len(yikes_json) < 100:
        my_books += ["ERROR"]
        return my_books
    yikes_json = yikes_json.split("}};")[0] + "}}"
    books = json.loads(yikes_json)
    if books:
        for book in books:
            correct_title = False;
            correct_author = True;
            book_info = books[book]
            od_title = book_info["title"].lower()
            #print("od: " + od_title)
            od_author = book_info["firstCreatorName"].lower()
            available = book_info["isAvailable"]
            if "cover300Wide" in book_info["covers"]:
                image_url = book_info["covers"]["cover300Wide"]["href"]
            else:
                image_url = ""
            link_url = root + "media/" + book_info["id"]
            if only_available and (not available):
                continue
            booktype = book_info["type"]["name"]
            #print("ebooks and audiobooks = " + str(not (ebooks and audiobooks)))
            #print("ebooks = " + str(ebooks and not (booktype.lower() == "ebook")))
            if not (ebooks and audiobooks):
                print(booktype.lower())
                if ebooks:
                    if booktype.lower() == "audiobook":
                        continue
                if audiobooks:
                    if booktype.lower() == "ebook":
                        continue
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
                my_books += [[author,title,link_url,image_url,available,booktype]]
                #print("True")
    return my_books

api_key = "Eny1ro9b7mxhs8CuFj2o6w"
api_secret = "bQKcvwYsv0ceEBjk95guDtguTXRUSgBxGPBT0YtxD6U"
user_id="43329866"    #ID of user to check the shelf of, can be found in url of user profile
gc = client.GoodreadsClient(api_key, api_secret)
user = gc.user(user_id)
all_books = []
my_books = user.per_shelf_reviews(shelf_name = "to-read")
#tbr=list(review.book for review in my_books if review.book['num_pages'] is not None)
tbr = list(review.book for review in my_books)
#tbr_bypages = sorted(tbr, key=lambda k: int(k['num_pages']))
#by_pages = list( int(book['num_pages']) for book in tbr if book['num_pages'] is not None)
categories = set()
outof = len(tbr)
i = 1
for book in tbr:
    title = book["title"]
    author = book["authors"]["author"]["name"]
    gr_id = int(book["id"]["#text"])
    gr_book = gc.book(gr_id)
    url = "https://www.goodreads.com/book/show.xml?v=2&key=" + api_key + "&id=" + str(gr_id)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'xml')
    book_info = soup.find_all('book')[0]
    genres_json = book_info.find_all('genre')
    genres = []
    for g in genres_json:
        genre = g.find('name').find_all(text=True)[0]
        genres += [genre]
    ser = soup.find('title').find_all(text=True)[0]
    series = False
    if '(' in ser:
        series = True
    #print(genres)
    #shelves = gr_book.popular_shelves[0:50]
    #categories.update(shelf['@name'] for shelf in shelves)
    try:
        temp_book = Book(title=title,author=author,pgcount=gr_book.num_pages,genres=genres,series=series)
    except:
        temp_book = Book(title=title,author=author,pgcount=None,genres=genres,series=series)
    
    all_books += [temp_book]
    #print(title + " by " + author)
#    root = "https://bpl.overdrive.com/"
#    results = libraryHas(title,author,root,only_available=True) 
#    if results and not (results[0] == 'ERROR'):
#        print(results)
    #libraryHas
    print( str(i) + "/" + str(outof))
    i += 1
    
#SAMPLE QUERY
fantasy_books = list(book for book in all_books if ('fantasy' in book.genres))
standalone_fantasy_books = list(book for book in fantasy_books if not book.series) #or
standalone_fantasy_books = list(book for book in all_books if ('fantasy' in book.genres) and (not book.series))
arr = list(book.genres for book in all_books)
genres = list( itertools.chain.from_iterable(arr) )
genres_set = set(genres)
genres = list(genres_set)