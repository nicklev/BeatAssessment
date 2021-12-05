import logging
import requests
from requests.sessions import HTTPAdapter, session

MIN_USER_KARMA = 2413
MAX_RESULTS = 50

session = requests.Session()
session.mount('https://', HTTPAdapter(pool_connections=10))


def getStories():
    stories = buildStories()
    return stories

# Creates the stories that will be returned to the user


def buildStories():

    # Two dimensional list.
    # Every row contains a list.
    # The first value refers to the number of comments and the second value to the position of this record in stories
    stories = {"stories": []}
    position = []
    count = 1
    newstories_ids = getNewStories()

    for story_id in newstories_ids:

        try:
            item = session.get(
                'https://hacker-news.firebaseio.com/v0/item/{id}.json'.format(id=story_id))

            logging.info("Latency on {URL}: {latency}".format(
                URL='https://hacker-news.firebaseio.com/v0/item/{id}.json'.format(id=story_id), latency=item.elapsed))

            item = item.json()
            username = item["by"]
            number_of_comments = item["descendants"]
            title = item["title"]

            user = session.get(
                'https://hacker-news.firebaseio.com/v0/user/{id}.json'.format(id=username))

            logging.info("Latency on {URL}: {latency}".format(
                URL='https://hacker-news.firebaseio.com/v0/user/{id}.json'.format(id=username), latency=user.elapsed))

            user = user.json()
            user_karma = user["karma"]

            if user_karma > MIN_USER_KARMA and count <= MAX_RESULTS:

                if len(position) == 0:
                    position.append([number_of_comments, count])
                else:
                    position = insertionSort(
                        position, number_of_comments, count)

                count += 1

                story = {"author": username, "karma": user_karma,
                         "comments": number_of_comments, "title": title, "position": None}
                stories["stories"].append(story)

        except TypeError as e:
            logging.error(e)
            continue
        except:
            logging.error("Fatal error.")

    stories_fixed_position = fixPositions(position, stories)
    return stories_fixed_position


def getNewStories():
    newstories_ids = session.get(
        'https://hacker-news.firebaseio.com//v0/newstories.json')

    logging.info("Latency on {URL}: {latency}".format(
        URL='https://hacker-news.firebaseio.com//v0/newstories.json', latency=newstories_ids.elapsed))

    newstories_ids = newstories_ids.json()
    return newstories_ids

# Sort position list based on number of comments


def insertionSort(position, number_of_comments, count):
    i = len(position) - 1
    key = number_of_comments
    while i >= 0 and key > position[i][0]:
        i -= 1
    position.insert(i+1, [key, count])
    return position

# fixPositions assigns the correct position for each story
# based on the number of comments


def fixPositions(position, stories):
    # "index" is the index of the "story" inside "stories" dictionary
    index = 1
    for story in stories["stories"]:
        for i in range(len(position)):
            if position[i][1] == index:
                story["position"] = i+1
        index += 1
    return stories
