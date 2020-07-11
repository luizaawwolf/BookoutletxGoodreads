from flask import Flask, render_template, request, redirect, url_for
import requests
import urllib.request
from bs4 import BeautifulSoup
from betterreads import client
import urllib.parse
import time
import json

app = Flask(__name__)


@app.route("/feedback",methods=['GET','POST'])
def getPage():
    return render_template("feedback.html")

@app.route("/", methods=['GET','POST'])
def home_view():
	if request.method == "GET":
		return render_template("main_page.html")
	user_id = int( request.form['user_id'] )
	to_read = bool( request.form.getlist('toread') )
	read = bool( request.form.getlist('read') )
	valid_books,error,successful_processes,shelf_size = getBooks(user_id=user_id,to_read=to_read,read=read)
	if shelf_size == -1:
		return render_template("main_page.html",successes="Oops! Looks like your profile is on private. You can change this in Goodreads -> Account Settings -> Settings -> Privacy")
	shelfs = ""
	if to_read and read:
		shelfs = "to-read and read shelf, "
	elif to_read:
		shelf = "to-read shelf, "
	else:
		shelf = "read shelf, "
	successes = "Out of the " + str(shelf_size) + " books processed from your Goodreads " + shelfs + str( successful_processes ) + " are on Book Outlet"
	return render_template("main_page.html",books=valid_books,err=error,successes=successes )

def getBooks(user_id,to_read,read):
	api_key = "Eny1ro9b7mxhs8CuFj2o6w"
	api_secret = "bQKcvwYsv0ceEBjk95guDtguTXRUSgBxGPBT0YtxD6U"
	gc = client.GoodreadsClient(api_key, api_secret)
	user = gc.user(user_id)
	if 'private' in list(user.__dict__['_user_dict'].keys()) and user.__dict__['_user_dict']['private'] == 'true':
		return [],[],[],-1
	#gr_books = user.per_shelf_reviews(shelf_name = "currently-reading")
	gr_books = []
	if to_read:
		gr_books += user.per_shelf_reviews(shelf_name = "to-read")
	if read:
		gr_books += user.per_shelf_reviews(shelf_name = "read")
	valid_books,error,successful_processes,shelf_size,leftover_books=getBooksHelper(gr_books)
	print(valid_books)
	print(error)
	print(successful_processes)
	print(shelf_size)
	return valid_books,error,successful_processes,shelf_size

def getBooksHelper(gr_books):
	valid_books = []
	error=False
	successful_processes = 0
	shelf_size = 0
	run_again = False
	max_time = 2.8 * 60
	start = time.time()
	leftover_books = []
	for book in gr_books:
		temp_book = book.book
		title = temp_book["title"]
		author = temp_book["authors"]["author"]["name"]
		#results = bookOutletHas(title=title, author=author)
		results = thriftBooksHas(title=title, author=author)
		if results:
			print(results)
			if results[0] == "ERROR":
			    error=True
			    continue
			else:
			    successful_processes += 1

		if results:
			for result in results:
				valid_books += [result]
		shelf_size += 1
		if time.time() - start > max_time:
			start_next = gr_books.index(book)
			leftover_books = gr_books[start_next:]
			break
	return valid_books,error,successful_processes,shelf_size,leftover_books

def bookOutletHas(title, author):
	title = title.split(" (")[0]
	title_url = urllib.parse.quote_plus(title)
	url = 'https://bookoutlet.com/Store/Search?qf=All&q=' + title_url
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	items = soup.findAll('div','grid-item')
	search_results = []
	if items and ( len(items[0]) < 2 ):
		search_results += ["ERROR"]
		return search_results
	correct_title = False;
	correct_author = True; #True
	for a in items:
	    ret_author = a.find('p','author').find_all(text=True)[0]
	    ret_author = ret_author.replace(",","")
	    ret_title = a.find('a','line-clamp-2').find_all(text=True)[0]
	    ret_title = ret_title.split("(")[0].strip()
	    price = a.find('div','price').find_all(text=True)[0]
	    title = title.split("(")[0].strip()
	    form = a.find('p','small').find_all(text=True)[0]
	    form = form.replace(")","").replace("(","")
	    if title.lower() == ret_title.lower():
	        print(ret_title.lower() + " by " + ret_author)
	        correct_title = True
	    else:
	        continue
	    for name in author.lower().split():
	        if name not in ret_author.lower().split():
	            correct_author = False
	    if( correct_title and correct_author):
	        link_url = "https://bookoutlet.com" + a.find_all('a',href=True)[0]['href']
	        image_url = "https:" + a.find_all('img')[0]['src']
	        search_results += [[author,title,link_url,image_url,price,form]]
	return search_results

def thriftBooksHas(title, author):
    search_results = [] 
    title = title.split(" (")[0]
    print("LOOKING FOR " + title)
    title_url = urllib.parse.quote_plus(title)
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
    url = 'https://www.thriftbooks.com/browse/?b.search=' + title_url + "t#b.s=mostPopular-desc&b.p=1&b.pp=30&b.oos&b.tile"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text,'html.parser')
    print(soup)
    if len(soup.findAll('script')) < 8:
    	print(title + " by " + author)
    	search_results += ["ERROR"]	#make more specific error?
    	return search_results
    script = str(soup.findAll('script')[8].string)
    script = script.split("window.searchStoreV2 = ")[1]
    script = script.replace("\r","").replace("\n","")
    script = script[script.find("\"works\":") + 8:script.find("};")].strip()
    script_dict = json.loads(script)
    i = 0
    for book_dict in script_dict:	
        correct_title = False;
        correct_author = True;
        ret_title = book_dict["title"]
        if title.lower() == ret_title.lower():
            correct_title = True
        else:
    	    continue
        if book_dict["availableCopies"] == 0:
        	continue
        ret_author = book_dict["authors"][0]["authorName"]
        print(ret_title.lower() + " by " + ret_author)
        image_url = book_dict["workImageLarge"]
        price = book_dict["lowPrice"]	
        form = book_dict["media"]
        for name in author.lower().split():
            if name not in ret_author.lower().split():
    	        correct_author = False
    	        continue
        if( correct_title and correct_author):
            links = soup.findAll('div',"AllEditionsItem-tileTitle")
            link_url = "https://www.thriftbooks.com" + links[i].find_all('a',href=True)[0]['href']
            search_results += [[author,title,link_url,image_url,price,form]]
            break
        i += 1
    return search_results