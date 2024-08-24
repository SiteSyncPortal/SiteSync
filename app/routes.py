from flask import Blueprint, render_template, request, redirect, url_for,flash
from app.models import get_projects, add_project_to_db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('login.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'partner' and password == "partner":  # Example check
            return redirect(url_for('main.partner_dashboard'))

    return render_template('login.html')

@main.route('/partner/dashboard', methods=['GET', 'POST'])
def partner_dashboard():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'view_projects':
            return redirect(url_for('main.projects'))

    return render_template('dashboard.html', title='Dashboard')

@main.route('/projects', methods=['GET'])
def projects():
    projects = get_projects()
    return render_template('projects.html', projects=projects)

@main.route('/add_project', methods=['POST'])
def add_project():
    # Get form data
    project_name = request.form.get('project_name').strip()
    location = request.form.get('location').strip()
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    status = request.form.get('status')

    # Condition 1: Start date should be less than end date
    if end_date and start_date >= end_date:
        flash("Start date must be earlier than the end date.")
        return redirect(url_for('main.projects'))

    # Condition 2: If status is "In Progress", set end date to None
    if status == "In Progress":
        end_date = None

    existing_projects = get_projects()
    for project in existing_projects:
        if project['project_name'].strip().lower() == project_name and project['location'].strip().lower() == location:
            flash("A project with the same name and location already exists.")
            return redirect(url_for('main.projects'))
        
    # Add the project to the database if all conditions are met
    add_project_to_db(project_name, location, start_date, end_date, status)
    return redirect(url_for('main.projects'))