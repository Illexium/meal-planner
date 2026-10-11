from collections import defaultdict
from datetime import date

from app.models import (
    InventoryItem,
    ShoppingList,
    ShoppingListItem
)


class ShoppingListService:

    @staticmethod
    def _build_inventory_stock():
        stock = defaultdict(list)

        inventory_items = InventoryItem.query.all()

        for item in inventory_items:
            stock[item.product_id].append(
                {
                    "quantity": float(item.quantity),
                    "expiration_date": item.expiration_date
                }
            )

        # Use products with earlier expiration dates first.
        # Items without expiration date are placed last.
        for product_id in stock:
            stock[product_id].sort(
                key=lambda lot: (
                    lot["expiration_date"] is None,
                    lot["expiration_date"] or date.max
                )
            )

        return stock

    @staticmethod
    def _consume_inventory(
        inventory_lots,
        required_quantity,
        meal_date
    ):
        remaining_required = required_quantity

        for lot in inventory_lots:

            if remaining_required <= 0:
                break

            expiration_date = lot["expiration_date"]

            # Product is considered usable on its expiration date.
            if (
                expiration_date is not None
                and expiration_date < meal_date
            ):
                continue

            available_quantity = lot["quantity"]

            if available_quantity <= 0:
                continue

            used_quantity = min(
                available_quantity,
                remaining_required
            )

            lot["quantity"] -= used_quantity
            remaining_required -= used_quantity

        return remaining_required

    @classmethod
    def calculate_missing_quantities(
        cls,
        meal_plan
    ):
        inventory_stock = cls._build_inventory_stock()

        missing = defaultdict(float)

        entries = sorted(
            meal_plan.entries,
            key=lambda entry: entry.meal_date
        )

        for entry in entries:
            recipe = entry.recipe

            for ingredient in recipe.ingredients:
                product = ingredient.product

                ingredient_unit = (
                    ingredient.ingredient_unit
                    .strip()
                    .lower()
                )

                product_unit = (
                    product.product_unit
                    .strip()
                    .lower()
                )

                if ingredient_unit != product_unit:
                    raise ValueError(
                        f"Unit mismatch for "
                        f"{product.product_name}."
                    )

                required_quantity = float(
                    ingredient.ingredient_quantity
                )

                inventory_lots = inventory_stock.get(
                    product.product_id,
                    []
                )

                missing_quantity = (
                    cls._consume_inventory(
                        inventory_lots,
                        required_quantity,
                        entry.meal_date
                    )
                )

                if missing_quantity > 0:
                    missing[
                        product.product_id
                    ] += missing_quantity

        return missing

    @classmethod
    def generate_shopping_list(
        cls,
        meal_plan
    ):
        missing = (
            cls.calculate_missing_quantities(
                meal_plan
            )
        )

        shopping_list = ShoppingList(
            meal_plan_id=meal_plan.meal_plan_id
        )

        for product_id, quantity in missing.items():

            if quantity <= 0:
                continue

            item = ShoppingListItem(
                product_id=product_id
            )

            item.update_quantity(
                round(quantity, 2)
            )

            shopping_list.items.append(item)

        return shopping_list
