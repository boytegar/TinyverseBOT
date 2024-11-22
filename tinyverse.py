import os
import sys
import random
import string
import requests
import time
import json
from datetime import datetime, timedelta
import requests

class TinyVerse:
    def __init__(self):
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Host': 'api.tonverse.app',
            'Origin': 'https://app.tonverse.app',
            'Referer': 'https://app.tonverse.app/',
            'sec-ch-ua-platform':'Windows',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
            'X-Requested-With': 'XMLHttpRequest'
        }
    
    def print_(self, word):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"[{now}] | {word}")

    def make_request(self, method, url, headers=None, json=None, data=None, params=None):
        retry_count = 0
        while True:
            time.sleep(2)
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, json=json)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=json, data=data, params=params)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=json, data=data)
            else:
                raise ValueError("Invalid method.")
            
            if response.status_code >= 500:
                if retry_count >= 4:
                    self.print_(f"Status Code: {response.status_code} | {response.text}")
                    return None
                retry_count += 1
            elif response.status_code >= 400:
                self.print_(f"Status Code: {response.status_code} | {response.text}")
                return None
            elif response.status_code >= 200:
                return response
    
    def auth(self, query):
        url = 'https://api.tonverse.app/auth/telegram'
        payload = {"data": query}
        headers = {
           **self.headers,
           'content-lenght': str(len(payload))
        }
        try:
            response = self.make_request('post',url=url, headers=headers, params=payload)
            if response is not None:
                return response.json()
            
        except Exception as error:
            self.print_(f"Error {error}")
            return None
    
    def begin(self, token, reff):
        url = 'https://api.tonverse.app/galaxy/begin'
        payload = {"session": token,
                   "stars": 100,
                   "referral": reff
                   }
        headers = {
           **self.headers,
           'content-lenght': str(len(payload))
        }
        try:
            response = self.make_request('post',url=url, headers=headers, params=payload)
            if response is not None:
                self.print_(f"Create account with reff {reff} done")
                return response.json()
            
        except Exception as error:
            self.print_(f"Error {error}")
            return None
    
    def get(self, token, id=None):
        url = 'https://api.tonverse.app/galaxy/get'
        payload = {"session": token,
                   "id": id,
                   "member_id": None
                   }
        headers = {
           **self.headers,
           'content-lenght': str(len(payload))
        }
        try:
            response = self.make_request('post',url=url, headers=headers, params=payload)
            if response is not None:
                jsons = response.json()
                responses = jsons.get('response',{})
                title = responses.get('title')
                member = responses.get('member')
                first_name = member.get('first_name')
                id = member.get('id')
                self.print_(f"Id : {id} | Name : {first_name} | {title}")
            
        except Exception as error:
            self.print_(f"Error {error}")
            return None
    
    def info(self, token):
        url = 'https://api.tonverse.app/user/info'
        payload = {"session": token,
                   "id": None,
                   "member_id": None
                   }
        headers = {
           **self.headers,
           'content-lenght': str(len(payload))
        }
        try:
            response = self.make_request('post',url=url, headers=headers, params=payload)
            if response is not None:
                jsons = response.json()
                responses = jsons.get('response',{})
                rating = responses.get('rating')
                dust = responses.get('dust')
                dust_max = responses.get('dust_max')
                dust_produce = responses.get('dust_produce')
                self.print_(f"Rating : {rating} | Dust : {dust}/{dust_max} | Produce : {dust_produce}")
                return dust


            
        except Exception as error:
            self.print_(f"Error {error}")
            return None
        

    def collect(self, token):
        url = 'https://api.tonverse.app/galaxy/collect'
        payload = {"session": token}
        headers = {
           **self.headers,
           'content-lenght': str(len(payload))
        }
        try:
            response = self.make_request('post',url=url, headers=headers, params=payload)
            if response is not None:
                jsons = response.json()
                responses = jsons.get('response',{})
                dust = responses.get('dust')
                self.print_(f"Collect Done get : {dust} Dust")
        except Exception as error:
            self.print_(f"Error {error}")
            return None
    
