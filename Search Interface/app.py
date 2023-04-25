# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 01:09:18 2020

@author: naren
"""

import pymongo
import pymysql
import pandas as pd
import json
from flask import *
from random import randint
app = Flask(__name__)

# Mongo db connection
DATABASE_NAME = "twitter_df"
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
        "searchText": "",
        "testItems" : []
    }
    return render_template("index.html", **responeData)

@app.route('/search', methods = ["GET","POST"])
def search():
    #get submit params
    searchText = str(request.form.get("searchText"))
    print('search start')
    print('searchText is :' + searchText)
    detailData = [ { "col1": "detail1", "col2": "detail2"}]
    testItems = [
                    { "col1" : "hahahahha" , "col2" : "3" , "detailDatas" : detailData },
                    { "col1" : "hahahahha2" , "col2" : "4",  "detailDatas" : detailData }
    ]
    responeData = {
        "searchText": searchText,
        "testItems" : testItems
    }
    return render_template("index.html", **responeData)
if __name__ == "__main__":
    app.run(debug=True)
