from rauth.service import OAuth1Service, OAuth1Session
import webbrowser
from betterreads import client
import requests
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse
import json
# Get a real consumer key & secret from: https://www.goodreads.com/api/keys
CONSUMER_KEY = 'Eny1ro9b7mxhs8CuFj2o6w'
CONSUMER_SECRET = 'bQKcvwYsv0ceEBjk95guDtguTXRUSgBxGPBT0YtxD6U'

goodreads = OAuth1Service(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    name='goodreads',
    request_token_url='https://www.goodreads.com/oauth/request_token',
    authorize_url='https://www.goodreads.com/oauth/authorize',
    access_token_url='https://www.goodreads.com/oauth/access_token',
    base_url='https://www.goodreads.com/'
    )

# head_auth=True is important here; this doesn't work with oauth2 for some reason
request_token, request_token_secret = goodreads.get_request_token(header_auth=True)

authorize_url = goodreads.get_authorize_url(request_token)
print('Visit this URL in your browser: ' + authorize_url)
webbrowser.open(authorize_url, new=0, autoraise=True)
accepted = 'n'
while accepted.lower() == 'n':
    # you need to access the authorize_link via a browser,
    # and proceed to manually authorize the consumer
    accepted = input('Have you authorized me? (y/n) ')
    
session = goodreads.get_auth_session(request_token, request_token_secret)
#
## book_id 631932 is "The Greedy Python"
data = {'name': 'to-read', 'book_id': 631932}
#
## add this to our "to-read" shelf
#response = session.post('https://www.goodreads.com/shelf/add_to_shelf.xml', data)
#
## these values are what you need to save for subsequent access.
ACCESS_TOKEN = session.access_token
ACCESS_TOKEN_SECRET = session.access_token_secret

gr_id = "16130758.xml"
url = "https://www.goodreads.com/book/show/" + gr_id
#data = {"id":gr_id,"key":CONSUMER_KEY}
response = session.get(url)
#response = requests.get(url)
soup = BeautifulSoup(response.text, 'xml')
brev = soup.find(id="bookReviews")
friends = brev.find_all("div", class_="friendReviews elementListBrown")
which_friends = []
for f in friends:
    friend = f.find_all('a')[0]['title']
    which_friends += [friend]
#print(soup)