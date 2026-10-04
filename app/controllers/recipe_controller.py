from flask import Blueprint, render_template, request, redirect, url_for

from app import db
from app.models import Recipe, Ingredient, Product


recipe_bp = Blueprint("recipes", __name__)


@recipe_bp.route("/recipes")
def recipe_list():
    recipes = Recipe.query.all()

    return render_template(
        "recipes.html",
        recipes=recipes
    )


@recipe_bp.route("/recipes/add", methods=["POST"])
def add_recipe():
    name = request.form["name"]
    description = request.form["description"]
    servings = request.form["servings"]

    recipe = Recipe()

    try:
        recipe.update_recipe(
            name,
            description,
            servings
        )
    except ValueError as error:
        return str(error), 400

    db.session.add(recipe)
    db.session.commit()

    return redirect(url_for("recipes.recipe_list"))


@recipe_bp.route(
    "/recipes/edit/<int:recipe_id>",
    methods=["GET", "POST"]
)
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        servings = request.form["servings"]

        try:
            recipe.update_recipe(
                name,
                description,
                servings
            )
        except ValueError as error:
            return str(error), 400

        db.session.commit()

        return redirect(url_for("recipes.recipe_list"))

    return render_template(
        "edit_recipe.html",
        recipe=recipe
    )


@recipe_bp.route("/recipes/<int:recipe_id>/ingredients")
def recipe_ingredients(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    products = Product.query.all()

    return render_template(
        "recipe_ingredients.html",
        recipe=recipe,
        products=products
    )


@recipe_bp.route(
    "/recipes/<int:recipe_id>/ingredients/add",
    methods=["POST"]
)
def add_ingredient(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    product_id = request.form["product_id"]
    quantity = request.form["quantity"]
    unit = request.form["unit"]

    ingredient = Ingredient(
        recipe_id=recipe.recipe_id
    )

    try:
        ingredient.update_ingredient(
            product_id,
            quantity,
            unit
        )
    except ValueError as error:
        return str(error), 400

    db.session.add(ingredient)
    db.session.commit()

    return redirect(
        url_for(
            "recipes.recipe_ingredients",
            recipe_id=recipe.recipe_id
        )
    )


@recipe_bp.route(
    "/recipes/<int:recipe_id>/ingredients/edit/<int:ingredient_id>",
    methods=["GET", "POST"]
)
def edit_ingredient(recipe_id, ingredient_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    ingredient = Ingredient.query.filter_by(
        ingredient_id=ingredient_id,
        recipe_id=recipe_id
    ).first_or_404()

    products = Product.query.all()

    if request.method == "POST":
        product_id = request.form["product_id"]
        quantity = request.form["quantity"]
        unit = request.form["unit"]

        try:
            ingredient.update_ingredient(
                product_id,
                quantity,
                unit
            )
        except ValueError as error:
            return str(error), 400

        db.session.commit()

        return redirect(
            url_for(
                "recipes.recipe_ingredients",
                recipe_id=recipe.recipe_id
            )
        )

    return render_template(
        "edit_ingredient.html",
        recipe=recipe,
        ingredient=ingredient,
        products=products
    )


@recipe_bp.route(
    "/recipes/<int:recipe_id>/ingredients/delete/<int:ingredient_id>",
    methods=["POST"]
)
def delete_ingredient(recipe_id, ingredient_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    ingredient = Ingredient.query.filter_by(
        ingredient_id=ingredient_id,
        recipe_id=recipe_id
    ).first_or_404()

    db.session.delete(ingredient)
    db.session.commit()

    return redirect(
        url_for(
            "recipes.recipe_ingredients",
            recipe_id=recipe.recipe_id
        )
    )


@recipe_bp.route(
    "/recipes/delete/<int:recipe_id>",
    methods=["POST"]
)
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    db.session.delete(recipe)
    db.session.commit()

    return redirect(url_for("recipes.recipe_list"))
