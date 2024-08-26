from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, request, session
from app.models import get_projects, add_project_to_db, delete_project_in_db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('login.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if (username == 'partner' and password == "partner") or (username == 'account' and password == "account"):  # Example check
            session['username'] = username
            return redirect(url_for('main.partner_dashboard'))
    print(username)
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
    username = session.get('username')
    return render_template('projects.html', projects=projects, username=username)

@main.route('/select_report')
def select_report():
    project_name = request.args.get('project_name')
    project_location = request.args.get('project_location')
    return render_template('select_report.html',project_name=project_name, project_location=project_location )

@main.route('/add_project', methods=['POST'])
def add_project():
    # Get form data
    project_name = request.form.get('project_name').strip()
    location = request.form.get('location').strip()
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    status = request.form.get('status')

    add_project_to_db(project_name, location, start_date, end_date, status)
    return redirect(url_for('main.projects'))

@main.route('/delete_project', methods=['POST'])
def delete_project():
    data = request.json
    project_id = data.get('project_id')
    
    if project_id:
        result = delete_project_in_db(project_id)
    if result['success']:
        return jsonify({'success': True})
    
    return jsonify({'success': False})
 
@main.route('/projects/<project_name>/<location>', methods=['GET', 'POST'])
def project_details(project_name, location):
    pl_value = 1000.00  # Example value, replace with actual logic
    total_pl_value = 5000.00  # Example value, replace with actual logic

    if request.method == 'POST':
        selected_date = request.form.get('calendar')
        flash(f"Selected date: {selected_date}")
    # Use the project_name and location parameters in your view logic
    return render_template('dpr.html', project_name=project_name, 
                           location=location, 
                           pl_value=pl_value, 
                           total_pl_value=total_pl_value)
   