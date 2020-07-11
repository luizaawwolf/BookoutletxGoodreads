# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 16:18:15 2020

@author: Luiza
"""

import requests
import xmltodict 
import json
from bs4 import BeautifulSoup


class GoodreadsRequest:
    def __init__(self, client, path, query_dict, req_format="xml"):
        """Initialize request object."""
        self.params = query_dict
        self.params.update(client.query_dict)
        self.host = client.base_url
        self.path = path
        self.req_format = req_format


#"user/show", {"id": user_id, "username": username}
    def request(self):
        resp = requests.get(self.host + self.path, params=self.params)
        print(self.params)
        print(self.host + self.path)
        soup = BeautifulSoup(resp.text, 'xml')
        print(soup)
        if resp.status_code != 200:
            print(resp)
            #raise GoodreadsRequestException(resp.reason, self.path)
        if self.req_format == "xml":
            data_dict = xmltodict.parse(resp.content, dict_constructor=dict)
            return data_dict["GoodreadsResponse"]
        elif self.req_format == "json":
            return json.loads(resp.content)
        else:
            raise Exception("Invalid format")


class GoodreadsClientException(Exception):
    def __init__(self, error_msg):
        self.error_msg = error_msg

    def __str__(self):
        return self.error_msg


class GoodreadsClient:
    base_url = "https://www.goodreads.com/"

    def __init__(self, client_key, client_secret):
        """Initialize the client"""
        self.client_key = client_key
        self.client_secret = client_secret
        
    @property
    def query_dict(self):
        return {"key": self.client_key}

    def request(self, *args, **kwargs):
        """Create a GoodreadsRequest object and make that request"""
        req = GoodreadsRequest(self, *args, **kwargs)
        return req.request()

    def user(self, user_id=None, username=None):
        """Get info about a member by id or username.

        If user_id or username not provided, the function returns the
        authorized user.
        """
        if not (user_id or username):
            return self.auth_user()
        resp = self.request("user/show", {"id": user_id, "username": username})
        return resp


api_key = "Eny1ro9b7mxhs8CuFj2o6w"
api_secret = "bQKcvwYsv0ceEBjk95guDtguTXRUSgBxGPBT0YtxD6U"
gc = GoodreadsClient(api_key, api_secret)
gc.user(user_id=43329866)