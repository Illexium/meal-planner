from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from app import db
from app.models import MealPlan, MealPlanEntry, Recipe


meal_plan_bp = Blueprint("meal_plans", __name__)


@meal_plan_bp.route("/meal-plans")
def meal_plan_list():
    meal_plans = MealPlan.query.all()

    return render_template(
        "meal_plans.html",
        meal_plans=meal_plans
    )


@meal_plan_bp.route(
    "/meal-plans/add",
    methods=["POST"]
)
def add_meal_plan():
    start_date = datetime.strptime(
        request.form["start_date"],
        "%Y-%m-%d"
    ).date()

    end_date = datetime.strptime(
        request.form["end_date"],
        "%Y-%m-%d"
    ).date()

    meal_plan = MealPlan()

    try:
        meal_plan.update_dates(
            start_date,
            end_date
        )
    except ValueError as error:
        return str(error), 400

    db.session.add(meal_plan)
    db.session.commit()

    return redirect(
        url_for("meal_plans.meal_plan_list")
    )


@meal_plan_bp.route(
    "/meal-plans/<int:meal_plan_id>"
)
def meal_plan_details(meal_plan_id):
    meal_plan = MealPlan.query.get_or_404(
        meal_plan_id
    )

    recipes = Recipe.query.all()

    return render_template(
        "meal_plan_details.html",
        meal_plan=meal_plan,
        recipes=recipes
    )


@meal_plan_bp.route(
    "/meal-plans/<int:meal_plan_id>/entries/add",
    methods=["POST"]
)
def add_meal_plan_entry(meal_plan_id):
    meal_plan = MealPlan.query.get_or_404(
        meal_plan_id
    )

    meal_date = datetime.strptime(
        request.form["meal_date"],
        "%Y-%m-%d"
    ).date()

    meal_type = request.form["meal_type"]
    recipe_id = request.form["recipe_id"]

    if not meal_plan.contains_date(meal_date):
        return (
            "Selected date is outside "
            "the meal plan period.",
            400
        )

    # Check that the selected recipe really exists
    Recipe.query.get_or_404(recipe_id)

    entry = MealPlanEntry(
        meal_plan_id=meal_plan.meal_plan_id
    )

    try:
        entry.update_entry(
            meal_date,
            meal_type,
            recipe_id
        )
    except ValueError as error:
        return str(error), 400

    db.session.add(entry)
    db.session.commit()

    return redirect(
        url_for(
            "meal_plans.meal_plan_details",
            meal_plan_id=meal_plan.meal_plan_id
        )
    )


@meal_plan_bp.route(
    "/meal-plans/<int:meal_plan_id>/entries/delete/"
    "<int:entry_id>",
    methods=["POST"]
)
def delete_meal_plan_entry(
    meal_plan_id,
    entry_id
):
    entry = MealPlanEntry.query.filter_by(
        entry_id=entry_id,
        meal_plan_id=meal_plan_id
    ).first_or_404()

    db.session.delete(entry)
    db.session.commit()

    return redirect(
        url_for(
            "meal_plans.meal_plan_details",
            meal_plan_id=meal_plan_id
        )
    )


@meal_plan_bp.route(
    "/meal-plans/delete/<int:meal_plan_id>",
    methods=["POST"]
)
def delete_meal_plan(meal_plan_id):
    meal_plan = MealPlan.query.get_or_404(
        meal_plan_id
    )

    db.session.delete(meal_plan)
    db.session.commit()

    return redirect(
        url_for("meal_plans.meal_plan_list")
    )


@meal_plan_bp.route(
    "/meal-plans/edit/<int:meal_plan_id>",
    methods=["GET", "POST"]
)
def edit_meal_plan(meal_plan_id):
    meal_plan = MealPlan.query.get_or_404(meal_plan_id)

    if request.method == "POST":
        start_date = datetime.strptime(
            request.form["start_date"],
            "%Y-%m-%d"
        ).date()

        end_date = datetime.strptime(
            request.form["end_date"],
            "%Y-%m-%d"
        ).date()

        try:
            meal_plan.update_dates(start_date, end_date)
        except ValueError as error:
            return str(error), 400

        for entry in meal_plan.entries:
            if not meal_plan.contains_date(entry.meal_date):
                return (
                    "Cannot change meal plan dates because "
                    "some planned meals would be outside "
                    "the new period.",
                    400
                )

        db.session.commit()

        return redirect(
            url_for("meal_plans.meal_plan_list")
        )

    return render_template(
        "edit_meal_plan.html",
        meal_plan=meal_plan
    )


@meal_plan_bp.route(
    "/meal-plans/<int:meal_plan_id>/entries/edit/<int:entry_id>",
    methods=["GET", "POST"]
)
def edit_meal_plan_entry(meal_plan_id, entry_id):
    meal_plan = MealPlan.query.get_or_404(meal_plan_id)

    entry = MealPlanEntry.query.filter_by(
        entry_id=entry_id,
        meal_plan_id=meal_plan_id
    ).first_or_404()

    recipes = Recipe.query.all()

    if request.method == "POST":
        meal_date = datetime.strptime(
            request.form["meal_date"],
            "%Y-%m-%d"
        ).date()

        meal_type = request.form["meal_type"]
        recipe_id = request.form["recipe_id"]

        if not meal_plan.contains_date(meal_date):
            return (
                "Selected date is outside "
                "the meal plan period.",
                400
            )

        Recipe.query.get_or_404(recipe_id)

        try:
            entry.update_entry(
                meal_date,
                meal_type,
                recipe_id
            )
        except ValueError as error:
            return str(error), 400

        db.session.commit()

        return redirect(
            url_for(
                "meal_plans.meal_plan_details",
                meal_plan_id=meal_plan_id
            )
        )

    return render_template(
        "edit_meal_plan_entry.html",
        meal_plan=meal_plan,
        entry=entry,
        recipes=recipes
    )
