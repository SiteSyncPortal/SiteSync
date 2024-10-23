from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import current_app, flash
from bson.objectid import ObjectId
from datetime import datetime
import pytz


def init_app(app):
    global client
    uri = app.config["MONGO_URI"]
    client = MongoClient(uri, server_api=ServerApi("1"))
    app.db = client.get_database("SiteSync")

    try:
        client.admin.command("ping")
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
        if (
            project["project_name"].strip().lower() == project_name
            and project["location"].strip().lower() == location
        ):
            flash("A project with the same name and location already exists.")
            return False

    project_id = current_app.db.projects.insert_one(
        {
            "project_name": project_name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "status": status,
        }
    ).inserted_id
    return project_id


def delete_project_in_db(project_id):
    result = current_app.db.projects.delete_one({"_id": ObjectId(project_id)})
    if result.deleted_count == 1:
        return {"success": True}
    else:
        return {"success": False}


def get_dpr_data(project_name, location):
    data = list(
        current_app.db.dpr.find({"Project": project_name, "location": location.upper()})
    )
    for item in data:
        item["_id"] = str(item["_id"])
        if item["Date"].count("-") != 2:
            continue
        day, month, year = item["Date"].split("-")
        item["Date"] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    return data


def get_inventory_data(project_name, location):
    data = list(
        current_app.db.inventory.find(
            {"project_name": project_name, "location": location}
        )
    )
    return data


def add_inventory_in_db(project_name, location, item_name, quantity, date):
    # Assume you have a UTC datetime from your database
    if len(date) == 0:
        utc_time = datetime.utcnow()
        # Convert UTC to a specific timezone (e.g., IST)
        timezone = pytz.timezone("Asia/Kolkata")
        local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(timezone)
        date = local_time.strftime("%Y-%m-%d")
        # Convert UTC to a specific timezone (e.g., IST)

    result = current_app.db.inventory.update_one(
        {"project_name": project_name, "location": location, "Item": item_name},
        {"$inc": {"Quantity": quantity}, "$max": {"Date": date}},
        upsert=True,
    )

    # Insert a timestamp record for this addition
    result = current_app.db.inventory_time_stamp.update_one(
        {
            "project_name": project_name,
            "location": location,
            "Item": item_name,
            "Date": date,  # Compare only the date
        },
        {
            "$set": {
                "Quantity": int(quantity),  # Update quantity
            }
        },
        upsert=True,  # This will insert if no matching document is found
    )
    return result


def get_matching_items(query):
    return current_app.db.inventory.distinct(
        "Item", {"Item": {"$regex": query, "$options": "i"}}
    )


# When clicking update button in account login
def update_inventory_in_db(project_name, location, items):
    try:
        # Assume you have a UTC datetime from your database
        utc_time = datetime.utcnow()
        # Convert UTC to a specific timezone (e.g., IST)
        timezone = pytz.timezone("Asia/Kolkata")
        local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(timezone)
        formatted_time = local_time.strftime("%Y-%m-%d")
        for item_name, new_quantity, old_quantity in items:
            # Update only if the quantity has changed
            print(item_name, new_quantity, old_quantity)
            if int(new_quantity) != int(old_quantity):
                result = current_app.db.inventory.update_one(
                    {
                        "project_name": project_name,
                        "location": location,
                        "Item": item_name,
                    },
                    {"$set": {"Quantity": int(new_quantity), "Date": formatted_time}},
                )

                if result.matched_count == 0:
                    return {
                        "success": False,
                        "message": f"Item '{item_name}' not found in inventory.",
                    }

                result = current_app.db.inventory_time_stamp.update_one(
                    {
                        "project_name": project_name,
                        "location": location,
                        "Item": item_name,
                        "Date": formatted_time,  # Compare only the date
                    },
                    {"$set": {"Quantity": int(new_quantity), "Date": formatted_time}},
                    upsert=True,  # This will insert if no matching document is found
                )

                if result.matched_count > 0:
                    print("Existing entry updated.")
                else:
                    print("New entry created.")

                return {"success": True, "message": "Inventory updated successfully!"}

    except Exception as e:
        print(f"Error updating inventory: {e}")
        return {
            "success": False,
            "message": "An error occurred while updating the inventory.",
        }


def delete_inventory_item_in_db(project_name, location, item_name):
    try:
        current_app.db.inventory.delete_one(
            {"project_name": project_name, "location": location, "Item": item_name}
        )
        current_app.db.inventory_time_stamp.delete_many(
            {"project_name": project_name, "location": location, "Item": item_name}
        )
        return {
            "success": True,
            "message": f"Item '{item_name}' deleted successfully.",
        }
    except Exception as e:
        print(f"Error deleting item: {e}")
        return {
            "success": False,
            "message": "An error occurred while deleting the item.",
        }


def get_inventory_timestamp_in_db(project_name, location):
    try:
        collection_str = "inventory_timestamp_" + project_name + "_" + location

        database = client["SiteSync"]
        collection_name = database[collection_str]
        print(collection_name)
        print(list(current_app.db.collection_name.find()))
    except Exception as e:
        print(e)

    pass


def get_inventory_by_timestamp(project_name, location, selected_date):

    timestamp_data = list(
        current_app.db.inventory_time_stamp.find(
            {
                "project_name": project_name,
                "location": location,
                "Date": selected_date,
            }
        )
    )
    # Convert ObjectId to string for each item
    for item in timestamp_data:
        item["_id"] = str(item["_id"])

    return timestamp_data


from flask import current_app
import calendar


def get_inventory_by_month(project_name, location, selected_month):
    # Query the inventory based on the month
    # Assume selected_month is in the format 'YYYY-MM'
    start_date = f"{selected_month}-01"
    end_date = f"{selected_month}-31"  # Assuming a month can have up to 31 days
    print("start_date==", start_date, end_date)
    inventory_data = list(
        current_app.db.inventory_time_stamp.find(
            {
                "project_name": project_name,
                "location": location,
                "Date": {"$gte": start_date, "$lte": end_date},
            }
        )
    )
    # Convert ObjectId to string and return data
    for item in inventory_data:
        item["_id"] = str(item["_id"])

    return inventory_data
