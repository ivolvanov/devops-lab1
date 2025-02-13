import os
import tempfile
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from functools import reduce


def setup_mongodb():
    uri = "mongodb://mongo:27017"
    client = MongoClient(uri)

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    # directly return the database
    db = client['devops-lab1']

    # we only have once collection, fetch it right away
    student_db = db['students']

    return student_db

student_db = setup_mongodb()

def add(student=None):
    query_d = {"first_name" : student.first_name, 
               "last_name" : student.last_name}
    res = student_db.find_one(query_d)
    if res:
        return 'already exists', 409

    doc_id = student_db.insert_one(student.to_dict())
    return student.student_id


def get_by_id(student_id=None, subject=None):
    query_d = {"student_id" : int(student_id)}
    student = student_db.find_one(query_d)
    if not student:
        return 'not found', 404
    # Remove the MongoDB ID and return json-serializable object
    del student['_id']
    return str(student)


def delete(student_id=None):
    query_d = {"student_id" : int(student_id)}
    student = student_db.find_one(query_d)
    if not student:
        return 'not found', 404
    student_db.delete_one(student)
    # Remove the MongoDB ID and return json-serializable object
    del student['_id']
    return str(student)
