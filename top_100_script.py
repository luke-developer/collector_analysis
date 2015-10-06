#############################################################
#                                                           #
#   Script created by Luke Adams                            #
#                                                           #
#   Takes a csv, cleans it and extracts top 100             #
#   words. Also functions to create database, table         #
#   and insert top 100 words and url into the database      #
#                                                           #
#############################################################


from __future__ import print_function
import sys
import mysql.connector
from mysql.connector import errorcode
import unicodecsv as csv
import csv as cc
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk import FreqDist
# need to set size limit to max otherwise we run into trouble
csv.field_size_limit(sys.maxsize)
# contains all the text data we need
indexed_body = {}
# custom tokenizer that get ONLY words from the webpages
custom_toke = RegexpTokenizer(r'[a-zA-Z]+')
# dictionary to hold our most frequent values and number or times occurs
fdlist = {}
# list to hold string of top words
body_val = []
# import and set our stop words
stops = set(stopwords.words('english'))

def clean_collector(collector):
    with open(collector,'rU') as f:
        csv = csv.reader(f)

        for i,row in enumerate(csv):
            try:
                server,body = row[6],row[0]
                body = custom_toke.tokenize(body)
                # get all words that are over 5 characters long to
                # eleminate random single characters and others that may be
                # meaningless and not be in the stop list
                body = [w for w in body if w not in stops and len(w) > 5]
                # calculate frequencies for all words that have made it past
                # the first test condition and put in body
                body = FreqDist(body)
                body = body.most_common(100)
            except IndexError:
                print("ERROR")
                continue

            if server not in indexed_body:
                indexed_body[server] = []
                indexed_body[server].append(body)

def create_db():
    config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'raise_on_warnings': True,
        }
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        sql = 'CREATE DATABASE top100'
        cursor.execute(sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Wrong username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()

def create_table():
    config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'top100',
        'raise_on_warnings': True,
        }
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        sql = 'CREATE TABLE wordbase(SNAME VARCHAR(255) NOT NULL,TOPWORDS MEDIUMTEXT NOT NULL, PRIMARY KEY(SNAME))'
        cursor.execute(sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Wrong username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()

def insert_into_db():
    config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'top100',
        'raise_on_warnings': True,
        }
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        # insert one by one
        for i in indexed_body:
            url = ''.join(i)
            for c in indexed_body[i]:
                y = [x[0] for x in c]
                body_val.append(', '.join(y))
                t = ','.join(y)
                sql = 'INSERT INTO wordbase(SNAME,TOPWORDS) VALUES(%s,%s)'
                cursor.execute(sql,(url,t))
                cursor.execute('COMMIT')     
        print("executed")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Wrong username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()

# function to enter list of list of tuples and then
# print out the strings contained; url and top words
def loop_through():
    for i in indexed_body:
        for c in indexed_body[i]:
            y = [x[0] for x in c]
            body_val.append(', '.join(y))

    for t in body_val:
        print(t)
