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


@product_bp.route(
    "/products/edit/<int:product_id>",
    methods=["GET", "POST"]
)
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        product.product_name = request.form["name"]
        product.product_category = request.form["category"]
        product.product_unit = request.form["unit"]

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
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    return redirect(url_for("products.product_list"))
