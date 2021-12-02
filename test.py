import requests
import json


def insertionSort(position, number_of_comments, count):

    i = len(position) - 1
    key = number_of_comments
    while i >= 0 and key < position[i][0]:
        i -= 1
    position.insert(i+1, [key, count])


def fix_positions(position, stories):
    index = 0
    for story in stories["stories"]:
        i = 0
        while i < len(position):
            if position[i][1] == index:
                story["position"] = i
            i += 1
        index += 1


newstories_ids = requests.get(
    'https://hacker-news.firebaseio.com//v0/newstories.json').json()

stories = {"stories": []}

# Two dimensional list.
# Every row contains a list.
# The first value refers to the number of comments and the second value to the position of this record in stories
position = []
count = 0

for story_id in newstories_ids:
    item = requests.get(
        'https://hacker-news.firebaseio.com/v0/item/{id}.json'.format(id=story_id)).json()

    username = item["by"]
    number_of_comments = item["descendants"]
    title = item["title"]
    # print(number_of_comments)
    # print(title)

    user = requests.get(
        'https://hacker-news.firebaseio.com/v0/user/{id}.json'.format(id=username)).json()
    user_karma = user["karma"]

    if user_karma > 2413 and count < 50:

        if len(position) == 0:
            position.append([number_of_comments, count])
        else:
            insertionSort(position, number_of_comments, count)

        count += 1

        story = {"author": username, "karma": user_karma,
                 "comments": number_of_comments, "title": title, "position": None}
        stories["stories"].append(story)

fix_positions(position, stories)
print(stories)
print("\n\n\n")
print(json.dumps(stories))
