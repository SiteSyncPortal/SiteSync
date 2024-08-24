from flask import Blueprint, render_template, request, redirect, url_for,jsonify
from app.models import get_projects
main = Blueprint('main', __name__)
mongo = PyMongo()
@main.route('/')
def home():
    return render_template('login.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Here you would typically verify the username and password against your database.
        # For simplicity, let's assume any username/password combination is correct.

        if username == 'partner' and password == "partner":  # Replace this with actual authentication logic
            return redirect(url_for('main.partner_dashboard'))

    # If the request is GET or the credentials are incorrect, re-render the login page.
    return render_template('login.html')

# @main.route('/partner/dashboard', methods=['GET','POST'])
# def partner_dashboard():
#     # Render the dashboard page after successful logi
        
#     return render_template('dashboard.html', title='Dashboard')

@main.route('/partner/dashboard', methods=['GET', 'POST'])
def partner_dashboard():
    if request.method == 'POST':
        action = request.form.get('action')

        # If the action is 'view_projects', redirect to the projects page
        if action == 'view_projects':
            return redirect(url_for('main.projects'))

    # Render the dashboard page by default
    return render_template('dashboard.html', title='Dashboard')

@main.route('/projects', methods=['GET'])
def projects():
    # This is where you'd typically query your database.
    # For example, if you're using PyMongo to query MongoDB:
    # projects = mongo.db.projects.find()

    # Dummy data for demonstration purposes:
    # projects = [
    #     {"name": "Project A", "status": "In Progress"},
    #     {"name": "Project B", "status": "Completed"},
    #     {"name": "Project C", "status": "Not Started"},
    # ]
    projects= get_projects()
    
    return render_template('projects.html', projects=projects) # Return the data as JSON


@main.route('/check_db_connection')
def check_db_connection():
    try:
        # Attempt to retrieve server status to check the connection
        server_status = mongo.db.command("serverStatus")
        return jsonify({"status": "Connected", "serverStatus": server_status})
    except Exception as e:
        return jsonify({"status": "Connection Failed", "error": str(e)}), 500