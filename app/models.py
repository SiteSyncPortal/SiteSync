from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import current_app 
from bson.objectid import ObjectId

# Initialize the MongoDB client and database connection
def init_app(app):
    uri = app.config["MONGO_URI"]
    client = MongoClient(uri, server_api=ServerApi('1'))
    app.db = client.get_database("SiteSync")  # Get the default database from the URI

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        print(f"Database name: {app.db.name}")  # Debugging: Check the database name
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")


def get_projects():
    projects = current_app.db.projects.find()
    return list(projects)

def add_project_to_db(project_name, location, start_date, end_date, status):
    project_id = current_app.db.projects.insert_one({
        'project_name': project_name,
        'location': location,
        'start_date': start_date,
        'end_date':end_date,
        'status':status
    }).inserted_id
    return project_id

def delete_project_in_db(project_id):
    # Delete the project from the database
    result = current_app.db.projects.delete_one({'_id': ObjectId(project_id)})

    if result.deleted_count == 1:
        return {'success': True}
    else:
        return {'success': False}
