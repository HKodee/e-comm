from app.decorators import admin_required
from flask import Blueprint, render_template
from flask_login import login_required
from app.models.User import User

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
    
@admin_bp.route("/user/<int:user_id>")
@login_required
@admin_required
def edit_user(user_id):

    user = User.query.get_or_404(user_id)

    return render_template(
        "admin/edit_user.html",
        user=user
    )