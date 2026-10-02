from app import db


class Product(db.Model):
    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    product_category = db.Column(db.String(100), nullable=False)
    product_unit = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Product {self.product_name}>"
