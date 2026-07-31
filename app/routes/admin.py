from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.decorators import admin_required
from app.extensions import db
from app.models import User,Employee


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
        user.role = request.form.get("role")
        db.session.commit()
        flash("User role updated successfully.", "success")
        
        return redirect(url_for("admin.users"))

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