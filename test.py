from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_pymongo import PyMongo

mongo = 

uri = "mongodb+srv://sitesyncportal:Sitesync_009@sitesync.n3awe.mongodb.net/?retryWrites=true&w=majority&appName=SiteSync"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print(mongo.db.projects.find())
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)