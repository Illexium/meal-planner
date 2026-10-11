from app import db


class ShoppingListItem(db.Model):
    __tablename__ = "shopping_list_items"

    shopping_list_item_id = db.Column(
        db.Integer,
        primary_key=True
    )

    shopping_list_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "shopping_lists.shopping_list_id"
        ),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.product_id"),
        nullable=False
    )

    quantity = db.Column(
        db.Float,
        nullable=False
    )

    is_purchased = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    product = db.relationship(
        "Product",
        backref="shopping_list_items"
    )

    def update_quantity(self, quantity):
        quantity = float(quantity)

        if quantity <= 0:
            raise ValueError(
                "Shopping list quantity "
                "must be greater than zero."
            )

        self.quantity = quantity

    def mark_as_purchased(self, purchased=True):
        self.is_purchased = bool(purchased)

    def __repr__(self):
        return (
            f"<ShoppingListItem "
            f"{self.shopping_list_item_id}>"
        )
