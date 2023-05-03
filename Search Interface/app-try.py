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
    else:
        cur.execute("SELECT userid_str, screen_name, name, favourites_count FROM users;")
        uer = pd.DataFrame(cur.fetchall(), columns=["userid_str", "screen_name", "name", "favourites_count"])
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
    twts = tweets.find(myquery).sort([("favorite_count", pymongo.DESCENDING), ("retweet_count", pymongo.DESCENDING)]).limit(10)

    testItems=twts

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
