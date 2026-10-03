from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///meal_planner.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.controllers.product_controller import product_bp
    from app.controllers.inventory_controller import inventory_bp

    app.register_blueprint(product_bp)
    app.register_blueprint(inventory_bp)

    @app.route("/")
    def home():
        return "Meal Planner is running!"

    return app
