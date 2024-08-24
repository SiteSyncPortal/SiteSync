from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Create a global PyMongo instance
mongo = PyMongo()

def init_app(app):
    global mongo
    mongo.init_app(app)

# def get_projects():
#     # Use the globally initialized mongo instance
#     projects = mongo.db.projects.find()
#     return list(projects)  # Convert the cursor to a list of projects
def get_projects():
    try:
        projects = mongo.db.projects.find()
        print(projects)
        return list(projects)
    except Exception as e:
        print(f"Error accessing MongoDB: {e}")
        return []

def add_project(name, description):
    # Use the globally initialized mongo instance
    project_id = mongo.db.projects.insert_one({
        'name': name,
        'description': description
    }).inserted_id
    return project_id
