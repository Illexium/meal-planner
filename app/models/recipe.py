from app import db


class Recipe(db.Model):
    __tablename__ = "recipes"

    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(100), nullable=False)
    recipe_descr = db.Column(db.Text, nullable=True)
    servings = db.Column(db.Integer, nullable=False)

    ingredients = db.relationship(
        "Ingredient",
        backref="recipe",
        cascade="all, delete-orphan"
    )

    def update_recipe(self, name, description, servings):
        name = name.strip()
        description = description.strip() if description else ""

        servings = int(servings)

        if not name:
            raise ValueError("Recipe name is required.")

        if servings <= 0:
            raise ValueError("Servings must be greater than zero.")

        self.recipe_name = name
        self.recipe_descr = description
        self.servings = servings

    def can_be_deleted(self):
        return True

    def __repr__(self):
        return f"<Recipe {self.recipe_name}>"
