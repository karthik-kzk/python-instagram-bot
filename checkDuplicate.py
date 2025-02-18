


import json


with open('top_posts_reddit.json', 'r') as file:
    data = json.load(file)




def normalized_str(String):
    return String.replace(" ", "").lower()


def isTitleDuplicate(String):
    for obj in data:
        if normalized_str(obj["title"]) == normalized_str(String):
            return True
    return False



