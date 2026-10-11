from app import db


class Ingredient(db.Model):
    __tablename__ = "ingredients"

    ingredient_id = db.Column(
        db.Integer,
        primary_key=True
    )

    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey("recipes.recipe_id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.product_id"),
        nullable=False
    )

    ingredient_quantity = db.Column(
        db.Float,
        nullable=False
    )

    ingredient_unit = db.Column(
        db.String(50),
        nullable=False
    )

    product = db.relationship(
        "Product",
        backref="ingredients"
    )

    def update_quantity(self, quantity):
        quantity = float(quantity)

        if quantity <= 0:
            raise ValueError(
                "Ingredient quantity must be greater than zero."
            )

        self.ingredient_quantity = quantity

    def update_ingredient(self, product, quantity):
        self.product = product
        self.update_quantity(quantity)

        # Unit always comes from Product
        self.ingredient_unit = product.product_unit

    def __repr__(self):
        return (
            f"<Ingredient "
            f"{self.ingredient_quantity} "
            f"{self.ingredient_unit}>"
        )
