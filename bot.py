import base64
import json
import os
import random
import sys
import time
from urllib.parse import parse_qs, unquote
from datetime import datetime, timedelta
from tinyverse import TinyVerse

def print_(word):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] | {word}")


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def load_query():
    try:
        with open('tinyverse_query.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print("File tinyverse_query.txt not found.")
        return [  ]
    except Exception as e:
        print("Failed get Query :", str(e))
        return [  ]

def parse_query(query: str):
    parsed_query = parse_qs(query)
    parsed_query = {k: v[0] for k, v in parsed_query.items()}
    user_data = json.loads(unquote(parsed_query['user']))
    parsed_query['user'] = user_data
    return parsed_query

def get(id):
        tokens = json.loads(open("tokens.json").read())
        if str(id) not in tokens.keys():
            return None
        return tokens[str(id)]

def save(id, token):
        tokens = json.loads(open("tokens.json").read())
        tokens[str(id)] = token
        open("tokens.json", "w").write(json.dumps(tokens, indent=4))

def load_config():
     data = json.loads(open("config.json").read())
     return data

def print_delay(delay):
    print()
    while delay > 0:
        now = datetime.now().isoformat(" ").split(".")[0]
        hours, remainder = divmod(delay, 3600)
        minutes, seconds = divmod(remainder, 60)
        sys.stdout.write(f"\r[{now}] | Waiting Time: {round(hours)} hours, {round(minutes)} minutes, and {round(seconds)} seconds")
        sys.stdout.flush()
        time.sleep(1)
        delay -= 1
    print_("Waiting Done, Starting....\n")

def main():
    while True:
        start_time = time.time()
        delay = 1 * 3700
        clear_terminal()
        queries = load_query()
        sum = len(queries)
        tinyverse = TinyVerse()
        config = load_config()
        for index, query in enumerate(queries):
            users = parse_query(query).get('user')
            id = users.get('id')
            print_(f"[SxG]======= Account {index+1}/{sum} [ {users.get('username','')} ] ========[SxG]")
            token = get(id)
            if token is None:
                print_("Get Token")
                data_auth = tinyverse.auth(query)
                response = data_auth.get('response')
                token = response.get('session')
                save(id, token)
                reff_id = config.get('reff_id')
                tinyverse.begin(token, reff_id)
                
            tinyverse.collect(token)
            tinyverse.get(token)
            tinyverse.info(token)
            
                

        end_time = time.time()
        total = delay - (end_time-start_time)
        if total > 0:
            print_delay(total)

if __name__ == "__main__":
     main()