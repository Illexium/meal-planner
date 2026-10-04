from app import db


class MealPlan(db.Model):
    __tablename__ = "meal_plans"

    meal_plan_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    entries = db.relationship(
        "MealPlanEntry",
        backref="meal_plan",
        cascade="all, delete-orphan"
    )

    def update_dates(self, start_date, end_date):
        if end_date < start_date:
            raise ValueError(
                "End date cannot be earlier than start date."
            )

        self.start_date = start_date
        self.end_date = end_date

    def contains_date(self, meal_date):
        return self.start_date <= meal_date <= self.end_date

    def __repr__(self):
        return (
            f"<MealPlan {self.start_date} - "
            f"{self.end_date}>"
        )
