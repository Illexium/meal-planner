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
    name = request.form["name"]
    category = request.form["category"]
    unit = request.form["unit"]

    product = Product(
        product_name=name,
        product_category=category,
        product_unit=unit
    )

    db.session.add(product)
    db.session.commit()

    return redirect(url_for("products.product_list"))
