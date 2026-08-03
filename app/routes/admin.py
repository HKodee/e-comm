from flask import Blueprint, request, flash, redirect, url_for, render_template
from flask_login import login_required
from app.decorators import admin_required
from app.extensions import db
from app.models import User, Employee, Product, Category


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():
    return render_template("admin/dashboard.html")

@admin_bp.route("/users")
@login_required
@admin_required
def users():

    all_users = User.query.order_by(User.id).all()

    return render_template(
        "admin/users.html",
        users=all_users
    )
    
@admin_bp.route("/user/<int:user_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_user(user_id):

    user = User.query.get_or_404(user_id)
    
    if request.method == "POST":
        user_id = request.form["user_id"]
        department = request.form["department"]
        designation = request.form["designation"]
        salary = float(request.form["salary"])
        
        existing_employee = Employee.query.filter_by(user_id=user_id).first()
        
        if existing_employee:
            flash("This user already has an employee profile.", "danger")
            return redirect(url_for("admin.add_employee"))
        
        employee = Employee(
            user_id=user_id,
            employee_code=f"HG{int(user_id):04}",
            department=department,
            designation=designation,
            salary=salary
        )

        db.session.add(employee)
        db.session.commit()

        flash("Employee added successfully!", "success")

        return redirect(url_for("admin.employee_list"))

    return render_template(
        "admin/edit_user.html",
        user=user
    )
    
@admin_bp.route("/employees")
@login_required
@admin_required
def employee_list():
    employees = Employee.query.all()

    return render_template(
        "admin/employee_list.html",
        employees=employees
    )
    
@admin_bp.route("/employees/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_employee():

    users = User.query.filter_by(role="employee").all()

    if request.method == "POST":

        user_id = request.form["user_id"]
        department = request.form["department"]
        designation = request.form["designation"]
        salary = float(request.form["salary"])

        # Check if employee already exists
        existing_employee = Employee.query.filter_by(user_id=user_id).first()

        if existing_employee:
            flash("This user already has an employee profile.", "danger")
            return redirect(url_for("admin.add_employee"))

        employee = Employee(
            user_id=user_id,
            employee_code=f"HG{int(user_id):04}",
            department=department,
            designation=designation,
            salary=salary
        )

        db.session.add(employee)
        db.session.commit()

        flash("Employee added successfully!", "success")

        return redirect(url_for("admin.employee_list"))

    return render_template(
        "admin/add_employee.html",
        users=users
    )

@admin_bp.route("/employees/edit/<int:employee_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_employee(employee_id):

    employee = Employee.query.get_or_404(employee_id)

    if request.method == "POST":

        employee.department = request.form["department"]
        employee.designation = request.form["designation"]
        employee.salary = float(request.form["salary"])

        db.session.commit()

        flash("Employee updated successfully!", "success")

        return redirect(url_for("admin.employee_list"))

    return render_template(
        "admin/edit_employee.html",
        employee=employee
    )
    
@admin_bp.route("/employees/<int:employee_id>")
@login_required
@admin_required
def view_employee(employee_id):

    employee = Employee.query.get_or_404(employee_id)

    return render_template(
        "admin/view_employee.html",
        employee=employee
    )