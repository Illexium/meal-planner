from datetime import date

from app import db


class ShoppingList(db.Model):
    __tablename__ = "shopping_lists"

    shopping_list_id = db.Column(
        db.Integer,
        primary_key=True
    )

    created_date = db.Column(
        db.Date,
        nullable=False,
        default=date.today
    )

    meal_plan_id = db.Column(
        db.Integer,
        db.ForeignKey("meal_plans.meal_plan_id"),
        nullable=False
    )

    meal_plan = db.relationship(
        "MealPlan",
        backref="shopping_lists"
    )

    items = db.relationship(
        "ShoppingListItem",
        backref="shopping_list",
        cascade="all, delete-orphan"
    )

    def clear_list(self):
        self.items.clear()

    def __repr__(self):
        return (
            f"<ShoppingList "
            f"{self.shopping_list_id}>"
        )
