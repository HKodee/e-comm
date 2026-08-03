from app.extensions import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(db.Text)

    price = db.Column(
        db.Float,
        nullable=False
    )

    stock = db.Column(
        db.Integer,
        default=0
    )

    image = db.Column(
        db.String(255)
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    category = db.relationship(
        "Category",
        back_populates="products"
    )

    def __repr__(self):
        return f"<Product {self.name}>"