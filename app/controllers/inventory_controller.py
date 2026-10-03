from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for

from app import db
from app.models import InventoryItem, Product


inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.route("/inventory")
def inventory_list():
    inventory_items = InventoryItem.query.all()
    products = Product.query.all()

    return render_template(
        "inventory.html",
        inventory_items=inventory_items,
        products=products
    )


@inventory_bp.route("/inventory/add", methods=["POST"])
def add_inventory_item():
    product_id = request.form["product_id"]
    quantity = request.form["quantity"]
    expiration_date = request.form["expiration_date"]

    expiration = None

    if expiration_date:
        expiration = datetime.strptime(
            expiration_date,
            "%Y-%m-%d"
        ).date()

    item = InventoryItem(
        product_id=product_id,
        expiration_date=expiration
    )

    try:
        item.update_quantity(quantity)
    except ValueError as error:
        return str(error), 400

    db.session.add(item)
    db.session.commit()

    return redirect(url_for("inventory.inventory_list"))


@inventory_bp.route(
    "/inventory/edit/<int:item_id>",
    methods=["GET", "POST"]
)
def edit_inventory_item(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    products = Product.query.all()

    if request.method == "POST":
        product_id = request.form["product_id"]
        quantity = request.form["quantity"]
        expiration_date = request.form["expiration_date"]

        expiration = None

        if expiration_date:
            expiration = datetime.strptime(
                expiration_date,
                "%Y-%m-%d"
            ).date()

        try:
            item.update_item(
                product_id,
                quantity,
                expiration
            )
        except ValueError as error:
            return str(error), 400

        db.session.commit()

        return redirect(url_for("inventory.inventory_list"))

    return render_template(
        "edit_inventory.html",
        item=item,
        products=products
    )


@inventory_bp.route(
    "/inventory/delete/<int:item_id>",
    methods=["POST"]
)
def delete_inventory_item(item_id):
    item = InventoryItem.query.get_or_404(item_id)

    db.session.delete(item)
    db.session.commit()

    return redirect(url_for("inventory.inventory_list"))
