from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    session,
)
from app.models import (
    get_projects,
    add_project_to_db,
    delete_project_in_db,
    get_dpr_data,
    get_inventory_data,
    add_inventory_in_db,
    get_matching_items,
    update_inventory_in_db,
    delete_inventory_item_in_db,
    get_inventory_timestamp_in_db,
    get_inventory_by_timestamp,
)

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("login.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if (username == "partner" and password == "partner") or (
            username == "account" and password == "account"
        ):
            session["username"] = username
            return redirect(url_for("main.partner_dashboard"))

    return render_template("login.html")


@main.route("/partner/dashboard", methods=["GET", "POST"])
def partner_dashboard():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "view_projects":
            return redirect(url_for("main.projects"))

    return render_template("dashboard.html", title="Dashboard")


@main.route("/projects", methods=["GET"])
def projects():
    projects = get_projects()
    username = session.get("username")
    return render_template("projects.html", projects=projects, username=username)


@main.route("/select_report")
def select_report():
    project_name = request.args.get("project_name")
    project_location = request.args.get("project_location")
    return render_template(
        "select_report.html",
        project_name=project_name,
        project_location=project_location,
    )


@main.route("/add_project", methods=["POST"])
def add_project():
    project_name = request.form.get("project_name").strip()
    location = request.form.get("location").strip()
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    status = request.form.get("status")

    add_project_to_db(project_name, location, start_date, end_date, status)
    return redirect(url_for("main.projects"))


@main.route("/delete_project", methods=["POST"])
def delete_project():
    data = request.json
    project_id = data.get("project_id")

    if project_id:
        result = delete_project_in_db(project_id)
    if result["success"]:
        return jsonify({"success": True})

    return jsonify({"success": False})


@main.route("/projects/<project_name>/<location>", methods=["GET", "POST"])
def project_details(project_name, location):
    pl_value = 1000.00
    total_pl_value = 5000.00

    dpr_data = get_dpr_data(project_name, location)
    dpr_dates = [item["Date"] for item in dpr_data]

    if request.method == "POST":
        selected_date = request.form.get("selected_date")
        project_name_input = request.form.get("project_name")
        flash(f"Selected date: {selected_date} for project: {project_name_input}")

    return render_template(
        "dpr.html",
        project_name=project_name,
        location=location,
        pl_value=pl_value,
        total_pl_value=total_pl_value,
        dpr_dates=dpr_dates,
        dpr_data=dpr_data,
    )


@main.route("/projects/<project_name>/<location>/Inventory", methods=["GET", "POST"])
def inventory(project_name, location):
    inventory_data = get_inventory_data(project_name, location)
    get_inventory_timestamp_in_db(project_name, location)
    item_suggestions = [item["Item"].lower() for item in inventory_data]
    return render_template(
        "inventory.html",
        project_name=project_name,
        location=location,
        inventory_data=inventory_data,
        item_suggestions=item_suggestions,
    )


@main.route("/projects/<project_name>/<location>/add_inventory", methods=["POST"])
def add_inventory(project_name, location):
    item_names = request.form.getlist("item_name[]")
    quantities = request.form.getlist("quantity[]")
    dates = request.form.getlist("date[]")

    for item_name, quantity, date in zip(item_names, quantities, dates):
        # Store the data in the inventory
        add_inventory_in_db(
            project_name, location, item_name.strip(), int(quantity), date
        )
        flash(f"{item_name}:{quantity} added successfully on {date}!")
    return redirect(
        url_for("main.inventory", project_name=project_name, location=location)
    )


@main.route("/fetch_item_suggestions", methods=["GET"])
def fetch_item_suggestions():
    query = request.args.get("query", "").strip().lower()
    if not query:
        return jsonify([])

    matching_items = get_matching_items(query)
    return jsonify(matching_items)


@main.route("/projects/<project_name>/<location>/update_inventory", methods=["POST"])
def update_inventory(project_name, location):
    item_names = request.form.getlist("item_name[]")
    new_quantities = request.form.getlist("quantity[]")
    old_quantities = request.form.getlist("old_quantity[]")

    # Pair item names with new and old quantities
    items = zip(item_names, new_quantities, old_quantities)
    result = update_inventory_in_db(project_name, location, items)

    if result["success"]:
        flash(result["message"], "success")
    else:
        flash(result["message"], "error")

    return redirect(
        url_for("main.inventory", project_name=project_name, location=location)
    )


@main.route(
    "/projects/<project_name>/<location>/delete_inventory_item", methods=["POST"]
)
def delete_inventory_item(project_name, location):
    data = request.json
    item_name = data.get("item_name")
    if item_name:
        result = delete_inventory_item_in_db(project_name, location, item_name)
        if result["success"]:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": result["message"]})

    return jsonify({"success": False, "message": "Item name not provided"})


@main.route(
    "/projects/<project_name>/<location>/fetch_inventory_by_date", methods=["GET"]
)
def fetch_inventory_by_date(project_name, location):
    selected_date = request.args.get("date")
    if not selected_date:
        return jsonify([])

    inventory_data = get_inventory_by_timestamp(project_name, location, selected_date)
    return jsonify(inventory_data)
