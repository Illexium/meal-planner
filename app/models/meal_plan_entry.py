from app import db


class MealPlanEntry(db.Model):
    __tablename__ = "meal_plan_entries"

    entry_id = db.Column(db.Integer, primary_key=True)

    meal_plan_id = db.Column(
        db.Integer,
        db.ForeignKey("meal_plans.meal_plan_id"),
        nullable=False
    )

    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey("recipes.recipe_id"),
        nullable=False
    )

    meal_date = db.Column(
        db.Date,
        nullable=False
    )

    meal_type = db.Column(
        db.String(30),
        nullable=False
    )

    recipe = db.relationship(
        "Recipe",
        backref="meal_plan_entries"
    )

    def assign_recipe(self, recipe_id):
        self.recipe_id = recipe_id

    def update_entry(self, meal_date, meal_type, recipe_id):
        meal_type = meal_type.strip()

        if not meal_type:
            raise ValueError("Meal type is required.")

        self.meal_date = meal_date
        self.meal_type = meal_type
        self.assign_recipe(recipe_id)

    def __repr__(self):
        return (
            f"<MealPlanEntry {self.meal_date} "
            f"{self.meal_type}>"
        )
