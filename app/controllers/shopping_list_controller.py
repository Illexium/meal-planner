from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from app import db
from datetime import datetime

from app.models import (
    MealPlan,
    ShoppingList,
    ShoppingListItem,
    InventoryItem
)

from app.services.shopping_list_service import (
    ShoppingListService
)


shopping_list_bp = Blueprint(
    "shopping_lists",
    __name__
)


@shopping_list_bp.route("/shopping-lists")
def shopping_list_list():
    shopping_lists = ShoppingList.query.all()
    meal_plans = MealPlan.query.all()

    return render_template(
        "shopping_lists.html",
        shopping_lists=shopping_lists,
        meal_plans=meal_plans
    )


@shopping_list_bp.route(
    "/shopping-lists/generate",
    methods=["POST"]
)
def generate_shopping_list():
    meal_plan_id = request.form["meal_plan_id"]

    meal_plan = MealPlan.query.get_or_404(
        meal_plan_id
    )

    try:
        shopping_list = (
            ShoppingListService
            .generate_shopping_list(
                meal_plan
            )
        )
    except ValueError as error:
        return str(error), 400

    db.session.add(shopping_list)
    db.session.commit()

    return redirect(
        url_for(
            "shopping_lists.shopping_list_details",
            shopping_list_id=(
                shopping_list.shopping_list_id
            )
        )
    )


@shopping_list_bp.route(
    "/shopping-lists/<int:shopping_list_id>"
)
def shopping_list_details(shopping_list_id):
    shopping_list = (
        ShoppingList.query.get_or_404(
            shopping_list_id
        )
    )

    return render_template(
        "shopping_list_details.html",
        shopping_list=shopping_list
    )


@shopping_list_bp.route(
    "/shopping-lists/"
    "<int:shopping_list_id>/items/"
    "<int:item_id>/toggle",
    methods=["POST"]
)
@shopping_list_bp.route(
    "/shopping-lists/"
    "<int:shopping_list_id>/items/"
    "<int:item_id>/purchase",
    methods=["POST"]
)
def purchase_shopping_list_item(
    shopping_list_id,
    item_id
):
    item = ShoppingListItem.query.filter_by(
        shopping_list_item_id=item_id,
        shopping_list_id=shopping_list_id
    ).first_or_404()

    purchased_quantity = request.form[
        "purchased_quantity"
    ]

    expiration_date = request.form.get(
        "expiration_date"
    )

    inventory_item = InventoryItem(
        product_id=item.product_id
    )

    try:
        inventory_item.update_quantity(
            purchased_quantity
        )
    except ValueError as error:
        return str(error), 400

    if expiration_date:
        inventory_item.expiration_date = (
            datetime.strptime(
                expiration_date,
                "%Y-%m-%d"
            ).date()
        )
    else:
        inventory_item.expiration_date = None

    item.mark_as_purchased(True)

    db.session.add(inventory_item)
    db.session.commit()

    return redirect(
        url_for(
            "shopping_lists.shopping_list_details",
            shopping_list_id=shopping_list_id
        )
    )


@shopping_list_bp.route(
    "/shopping-lists/"
    "<int:shopping_list_id>/clear",
    methods=["POST"]
)
def clear_shopping_list(shopping_list_id):
    shopping_list = (
        ShoppingList.query.get_or_404(
            shopping_list_id
        )
    )

    shopping_list.clear_list()
    db.session.commit()

    return redirect(
        url_for(
            "shopping_lists.shopping_list_details",
            shopping_list_id=shopping_list_id
        )
    )


@shopping_list_bp.route(
    "/shopping-lists/"
    "delete/<int:shopping_list_id>",
    methods=["POST"]
)
def delete_shopping_list(shopping_list_id):
    shopping_list = (
        ShoppingList.query.get_or_404(
            shopping_list_id
        )
    )

    db.session.delete(shopping_list)
    db.session.commit()

    return redirect(
        url_for(
            "shopping_lists.shopping_list_list"
        )
    )
