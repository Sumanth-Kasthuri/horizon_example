"""
Author: Archie Jarvis
Student ID: 20022663
"""

from app.core.database.models import Recipe
from app.core.service import Service
from app.core.services.restaurant_service import RestaurantService


class MenuManager:
    def __init__(self, app):
        self.__app = app

    def is_menu_item_suitable_for(self, dietary_requirements, recipe_id):
        """
        Returns whether the given menu item is suitable for the given dietary requirements.
        :param recipe_id:
        :param dietary_requirements: The dietary requirements object.
        :return: Whether the menu item is suitable for the given dietary requirements.
        """

        with Service(self.__app.get_session(), Recipe) as recipe_service:
            recipe = recipe_service.get_by_id(recipe_id)

            for col in dietary_requirements.__table__.columns:
                if col.name == "id" or col.name == "stock_item_id":
                    continue

                for recipe_item in recipe.recipe_items:
                    stock_item = recipe_item.stock_item
                    if not (
                        not getattr(dietary_requirements, col.name)
                        and getattr(stock_item.dietary_requirements, col.name)
                    ):
                        return False
        return True

    def get_suitable_food_items(self, dietary_requirements, restaurant_id):
        """
        Returns the suitable food items for the given dietary requirements.
        :param dietary_requirements: The dietary requirements object.
        :param restaurant_id: The restaurant id to get the suitable food items for.
        :return: list of recipe ids that are safe for the given dietary requirements.
        """
        with RestaurantService(self.__app.get_session()) as restaurant_service:
            restaurant = restaurant_service.get_by_id(restaurant_id)

            suitable_recipes = []
            for food_category in restaurant.menu.food_categories:
                for recipe in food_category.recipes:
                    if self.is_menu_item_suitable_for(dietary_requirements, recipe.id):
                        suitable_recipes.append(recipe)
            return suitable_recipes
