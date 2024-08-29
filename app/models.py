from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import current_app, flash
from bson.objectid import ObjectId

def init_app(app):
    uri = app.config["MONGO_URI"]
    client = MongoClient(uri, server_api=ServerApi('1'))
    app.db = client.get_database("SiteSync")

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")

def get_projects():
    projects = current_app.db.projects.find()
    return list(projects)

def add_project_to_db(project_name, location, start_date, end_date, status):
    if end_date and start_date >= end_date:
        flash("Start date must be earlier than the end date.")
        return False

    if status == "In Progress":
        end_date = None

    existing_projects = get_projects()
    for project in existing_projects:
        if project['project_name'].strip().lower() == project_name and project['location'].strip().lower() == location:
            flash("A project with the same name and location already exists.")
            return False
        
    project_id = current_app.db.projects.insert_one({
        'project_name': project_name,
        'location': location,
        'start_date': start_date,
        'end_date':end_date,
        'status':status
    }).inserted_id
    return project_id

def delete_project_in_db(project_id):
    result = current_app.db.projects.delete_one({'_id': ObjectId(project_id)})
    if result.deleted_count == 1:
        return {'success': True}
    else:
        return {'success': False}

def get_dpr_data(project_name, location):
    data = list(current_app.db.dpr.find({"Project": project_name, "location": location.upper()}))
    for item in data:
        item['_id'] = str(item['_id'])
        if item['Date'].count('-') != 2:
            continue
        day, month, year = item['Date'].split('-')
        item['Date'] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    return data

def get_inventory_data(project_name, location):
    data = list(current_app.db.inventory.find({"Project": project_name, "location": location}))
    return data

def add_inventory_in_db(project_name, location, item_name, quantity):
    result = current_app.db.inventory.update_one(
        {"Project": project_name, "location": location, "Item": item_name},
        {"$inc": {"Quantity": quantity}},
        upsert=True
    )
    return result

def get_matching_items(query):
    return current_app.db.inventory.distinct("Item", {"Item": {"$regex": query, "$options": "i"}})

def update_inventory_in_db(project_name, location, items):
    try:
        for item_name, new_quantity, old_quantity in items:
            # Update only if the quantity has changed
            if int(new_quantity) != int(old_quantity):
                result = current_app.db.inventory.update_one(
                    {"Project": project_name, "location": location, "Item": item_name},
                    {"$set": {"Quantity": int(new_quantity)}}
                )
            
                if result.matched_count == 0:
                    return {'success': False, 'message': f"Item '{item_name}' not found in inventory."}
            
        return {'success': True, 'message': "Inventory updated successfully!"}
    
    except Exception as e:
        print(f"Error updating inventory: {e}")
        return {'success': False, 'message': "An error occurred while updating the inventory."}

