# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 01:09:18 2020

@author: naren
"""

import pymongo
import pymysql
import redis
import pandas as pd
import json
from flask import *
from random import randint
app = Flask(__name__)

# Mongo db connection
DATABASE_NAME = "DBMS"
COLLECTION_NAME = "tweet"

client = pymongo.MongoClient()
db = client[DATABASE_NAME]
tweets = db[COLLECTION_NAME]

# MySQL db connection
conn = pymysql.connect(host='localhost', port=3306, user='root', password="19989797", charset="utf8mb4", database='db1')
cur = conn.cursor()

@app.route('/')
def homePage():
    responeData = {
        "search_keyword": "",
        "search_hashtag": "",
        "search_user": "",
        "start_at": "",
        "end_at": "",
        "testItems": []
    }
    return render_template("index-1.html", **responeData)

@app.route('/search', methods = ["GET","POST"])
def search():
    #get submit params
    search_keyword = str(request.form.get("search_keyword"))
    search_hashtag = str(request.form.get("search_hashtag"))
    search_user = str(request.form.get("search_user"))
    start_at = str(request.form.get("start_at"))
    end_at = str(request.form.get("end_at"))
    print('search start')
    print(
        'keyword is :' + search_keyword +
        'hashtag is :' + search_hashtag +
        'user is :' + search_user +
        'start time is :' + start_at +
        'end time is :' + end_at
    )

    #searching part
    myquery = {}
    # search for keyword
    if search_user != "":
        # my sql
        cur.execute("SELECT userid_str, screen_name, name, favourites_count FROM users WHERE screen_name = %s;",
                    (search_user,))
        uer = pd.DataFrame(cur.fetchall(), columns=["userid_str", "screen_name", "name", "favourites_count"])
        # mongodb
        userid_str = uer["userid_str"].tolist()
        myquery["user.id_str"] = {"$in": userid_str}
    if search_keyword != "":
        myquery["$text"] = {"$search": search_keyword}
    if search_hashtag != "":
        myquery["entities.hashtags.text"] = search_hashtag
        # time range
    if start_at and end_at != "":
        myquery['created_at'] = {'$gte': start_at, '$lte': end_at}
    elif start_at != "":
        myquery['created_at'] = {'$gte': start_at}
    elif end_at != "":
        myquery['created_at'] = {'$lte': end_at}
    twts = tweets.find(myquery)

    # get users' information
    def get_user_info(user_id):
        cur.execute("SELECT * FROM users WHERE userid_str = %s;",
                    (user_id,))
        user_info = cur.fetchone()
        if user_info is not None:
            return {
                "userid_str": user_info[0],
                "screen_name": user_info[1],
                "name": user_info[2],
                "followers_count": user_info[3],
                "favourites_count": user_info[4],
                "statuses_count": user_info[5]
            }
        return None

    testItems = []
    for tweet in twts:
        tweet_user_id = tweet["user"]["id_str"]
        user_info = get_user_info(tweet_user_id)
        if user_info is not None:
            tweet["user_info"] = user_info
        testItems.append(tweet)

    testItems = sorted(testItems, key=lambda x: (x['user_info']['followers_count'], x['user_info']['favourites_count']), reverse=True)
    testItems = testItems[:5]

    responeData = {
        "search_keyword": search_keyword,
        "search_hashtag": search_hashtag,
        "search_user": search_user,
        "start_at": start_at,
        "end_at": end_at,
        "testItems": testItems
    }
    return render_template("index-1.html", **responeData)


if __name__ == "__main__":
    app.run(debug=True)
