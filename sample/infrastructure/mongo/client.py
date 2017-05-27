from pymongo.mongo_client import MongoClient
"""
Created on May 26, 2017

@author: Erick Cellani
"""


def connect(uri):
    try:
        return MongoClient(uri)
    except Exception as e:
        raise e
