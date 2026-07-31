from datetime import date
from app.extensions import db


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        unique=True,
        nullable=False
    )

    employee_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    designation = db.Column(
        db.String(100),
        nullable=False
    )

    department = db.Column(
        db.String(100),
        nullable=False
    )

    salary = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    joining_date = db.Column(
        db.Date,
        nullable=False,
        default=date.today
    )

    shift = db.Column(
        db.String(30),
        nullable=False,
        default="Morning"
    )

    upi_id = db.Column(
        db.String(100)
    )

    emergency_contact = db.Column(
        db.String(20)
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    def __repr__(self):
        return f"<Employee {self.employee_code}>"