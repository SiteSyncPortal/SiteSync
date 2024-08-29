from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, request, session
from app.models import get_projects, add_project_to_db, delete_project_in_db, get_dpr_data, get_inventory_data,add_inventory_in_db,sell_inventory_in_db,get_matching_items

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

    # Get the DPR data (dates)
    dpr_data = get_dpr_data(project_name, location)
    dpr_dates = [item['Date'] for item in dpr_data]

    if request.method == 'POST':
        selected_date = request.form.get('selected_date')
        project_name_input = request.form.get('project_name')
        # Handle the form submission logic here
        flash(f"Selected date: {selected_date} for project: {project_name_input}")

    return render_template('dpr.html', project_name=project_name, 
                           location=location, 
                           pl_value=pl_value, 
                           total_pl_value=total_pl_value,
                           dpr_dates=dpr_dates,
                           dpr_data=dpr_data)
    
@main.route('/projects/<project_name>/<location>/Inventory', methods=['GET', 'POST'])
def inventory(project_name, location):
    inventory_data = get_inventory_data(project_name, location)
    
    # Extract item names for suggestions
    item_suggestions = [item['Item'].lower() for item in inventory_data]
    return render_template('inventory.html', 
                           project_name=project_name, 
                           location=location, 
                           inventory_data=inventory_data, 
                           item_suggestions=item_suggestions)



@main.route('/projects/<project_name>/<location>/add_inventory', methods=['POST'])
def add_inventory(project_name, location):
    item_names = request.form.getlist('item_name[]')
    quantities = request.form.getlist('quantity[]')

    for item_name, quantity in zip(item_names, quantities):
        add_inventory_in_db(project_name, location, item_name.strip(), int(quantity))
        flash(f'{item_name}:{quantity} added successfully!')
    return redirect(url_for('main.inventory', project_name=project_name, location=location))

@main.route('/projects/<project_name>/<location>/sell_inventory', methods=['POST'])
def sell_inventory(project_name, location):
    item_names = request.form.getlist('item_name[]')
    quantities = request.form.getlist('quantity[]')
    flag = 0
    for item_name, quantity in zip(item_names, quantities):
        result = sell_inventory_in_db(project_name, location, item_name.strip(), int(quantity))
        
        if not result['success']:
            flash(result['message'])
            flag = 1
    if flag == 0:
        flash('Inventory sold successfully!')
        
    return redirect(url_for('main.inventory', project_name=project_name, location=location))

@main.route('/fetch_item_suggestions', methods=['GET'])
def fetch_item_suggestions():
    query = request.args.get('query', '').strip().lower()
    print("hi",query)
    if not query:
        return jsonify([])

    # Fetch items from inventory that match the query
    matching_items = get_matching_items(query) 
   
    return jsonify(matching_items)
