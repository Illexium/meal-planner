from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Product

product_bp = Blueprint("products", __name__)


@product_bp.route("/products")
def product_list():
    products = Product.query.all()
    return render_template("products.html", products=products)


@product_bp.route("/products/add", methods=["POST"])
def add_product():
    name = request.form["name"].strip()
    category = request.form["category"].strip()
    unit = request.form["unit"].strip()

    if not name or not category or not unit:
        return "All product fields are required.", 400

    product = Product(
        product_name=name,
        product_category=category,
        product_unit=unit
    )

    db.session.add(product)
    db.session.commit()

    return redirect(url_for("products.product_list"))


@product_bp.route(
    "/products/edit/<int:product_id>",
    methods=["GET", "POST"]
)
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        name = request.form["name"].strip()
        category = request.form["category"].strip()
        unit = request.form["unit"].strip()

        if not name or not category or not unit:
            return "All product fields are required.", 400

        product.update_product(name, category, unit)

        db.session.commit()

        return redirect(url_for("products.product_list"))

    return render_template(
        "edit_product.html",
        product=product
    )


@product_bp.route(
    "/products/delete/<int:product_id>",
    methods=["POST"]
)
@product_bp.route(
    "/products/delete/<int:product_id>",
    methods=["POST"]
)
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    if not product.can_be_deleted():
        return (
            "Cannot delete product because it is used in inventory.",
            400
        )

    db.session.delete(product)
    db.session.commit()

    return redirect(url_for("products.product_list"))
