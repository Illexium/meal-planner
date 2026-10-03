from app import db


class InventoryItem(db.Model):
    __tablename__ = "inventory_items"

    inventory_item_id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.product_id"),
        nullable=False
    )

    quantity = db.Column(db.Float, nullable=False)
    expiration_date = db.Column(db.Date, nullable=True)

    product = db.relationship(
        "Product",
        backref="inventory_items"
    )

    def update_quantity(self, quantity):
        quantity = float(quantity)

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        self.quantity = quantity

    def update_item(self, product_id, quantity, expiration_date):
        self.product_id = product_id
        self.update_quantity(quantity)
        self.expiration_date = expiration_date

    def __repr__(self):
        return f"<InventoryItem {self.inventory_item_id}>"
