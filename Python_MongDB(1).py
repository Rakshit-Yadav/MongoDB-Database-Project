# -*- coding: utf-8 -*-

# -- Sheet --

import pymongo
from pymongo import MongoClient

# Connecting to MondoDB Atlas


conn_str = "mongodb+srv://username:password@cluster0.xjojr.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(conn_str, serverSelectionTimeoutMS=5000)
try:
    print(client.server_info())
except Exception:
    print("Unable to connect to the server.")

#List names of database

database_list = client.list_database_names()
print(database_list)

# Drop the OnlineStore database if already exist

client.drop_database("OnlineStore")

# List database again to ensure the OnlineStore database is deleted

database_list = client.list_database_names()
print(database_list)

# Creating a Database, Collection and Inserting a Document -- Using Dictionary Method


myDB = client["OnlineStore"]
myCollection = myDB["phones.items"]
item_1 = {
"_id" : "U1IT00007",
"item_name" : "iPhone 13",
"max_discount" : "10%",
"batch_number" : "RR450020FRG",
"price" : 1280,
"category" : "electronic"
}
myCollection.insert_one(item_1)
print(myCollection.inserted_id)

# Creating a Database, Collection and Inserting a Document -- Using Attribute Method


myDB = client.OnlineStore
myCollection = myDB.laptops.items
item_1 = {
"_id" : "U1IT00008",
"item_name" : "MacBook Pro 2",
"max_discount" : "20%",
"batch_number" : "RR450020FAW",
"price" : 1080,
"category" : "electronic"
}
myCollection.insert_one(item_1)
print(myCollection.inserted_id)

# Retrieving Document from Collection -- Using Dictionary Method


import pprint
myCollection1 = myDB["phones.items"]
phones_items = myCollection1.find()
for item1 in phones_items:
    pprint.pprint(item1)
    

# Retrieving Document from Collection -- Using Attribute Method


myCollection2 = myDB.laptops.items
laptops_items = myCollection2.find()
for item2 in laptops_items:
    pprint.pprint(item2)
    #pprint.pprint(item2["item_name"])

# Printing a Value from a Document in Doctionary style


myCollection = myDB.phones.items
phones_items = myCollection.find()
for items in phones_items:
    print( items["item_name"] + " is in the " + items["category"] + " category")

# Creating an Arrays of Ducuments for Insertion Into OnlineStore Database


item_2 = {
"_id" : "U1IT00010",
"item_name" : "Samsong Note 5",
"max_discount" : "5%",
"batch_number" : "RR45054FSR",
"price" : 480,
"category" : "electronic"
}

item_3 = {
"_id" : "U1IT00020",
"item_name" : "Nokia X",
"max_discount" : "10%",
"batch_number" : "RR450020FRG",
"price" : 1280,
"category" : "Electronic"
}

item_4 = {
"_id" : "U1IT00021",
"item_name" : "Sony Xperia",
"max_discount" : "10%",
"batch_number" : "RR450020FRG",
"price" : 720,
"category" : "Electronic"
}

item_5 = {
"_id" : "U1IT00022",
"item_name" : "Blackberry 2",
"max_discount" : "10%",
"batch_number" : "RR450020FRG",
"price" : 880,
"category" : "Electronic"
}

new_items = [item_2, item_3, item_4, item_5]
pprint.pprint(new_items)

# Inserting Multiple Documents In User1.items Collection


myDB = client["OnlineStore"]
myCollection = myDB["phones.items"]
myCollection.insert_many(new_items)

# Converting MongoDB document (Dictionary) Into Pandas Dataframe


import pandas as pd
all_items = myCollection.find()
items_df = pd.DataFrame(all_items)
items_df

# Close connection

client.close()

# End.


