# test code

import logging
import json
arr=[1,2,3]

with open('top_posts_reddit.json', 'r') as file:
    data = json.load(file)

obj={
    "title": "Gentleman",
    "url": "https://v.redd.it/6eycfeqpjnje1",
    "score": 1016,
    "author": "EthanWilliams_TG",
    "created_utc": 1739777493.0,
    "comments": 27
}


def normalized_str(String):
    return String.replace(" ", "").lower()
def isTitleDuplicate(String):
    for obj in data:
        if normalized_str(obj["title"]) == normalized_str(String):
            return True
    return False
        

print(len())
