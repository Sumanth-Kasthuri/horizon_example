"""
Author: Archie Jarvis
Student ID: 20022663
"""

import secrets
from datetime import datetime

from passlib.handlers.sha2_crypt import sha256_crypt
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    Float,
    Date,
    Time,
    DateTime,
)
from sqlalchemy import Table as ALTable
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

recipe_order_association = ALTable(
    "recipe_order_association",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("recipe_id", Integer, ForeignKey("recipes.id")),
    Column("order_id", Integer, ForeignKey("orders.id")),
    Column("timestamp", DateTime, default=datetime.now()),
)


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String, unique=True)
    password = Column(String)
    salt = Column(String)

    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    restaurant = relationship("Restaurant", backref="accounts")

    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="accounts", uselist=False)

    def __init__(self, username, password):
        self.username = username
        self.salt = secrets.token_hex(16)
        self.password = sha256_crypt.hash(password + self.salt)

    def is_admin(self):
        return self.role.admin if self.role else False


class DietaryRequirement(Base):
    __tablename__ = "dietary_requirements"

    id = Column(Integer, primary_key=True)

    stock_item_id = Column(Integer, ForeignKey("stock_items.id"))
    stock_item = relationship(
        "StockItem", back_populates="dietary_requirements", uselist=False
    )

    celery = Column(Boolean, nullable=False, default=True)
    crustaceans = Column(Boolean, nullable=False, default=True)
    eggs = Column(Boolean, nullable=False, default=True)
    fish = Column(Boolean, nullable=False, default=True)
    lupin = Column(Boolean, nullable=False, default=True)
    milk = Column(Boolean, nullable=False, default=True)
    molluscs = Column(Boolean, nullable=False, default=True)
    mustard = Column(Boolean, nullable=False, default=True)
    nuts = Column(Boolean, nullable=False, default=True)
    peanuts = Column(Boolean, nullable=False, default=True)
    sesame_seeds = Column(Boolean, nullable=False, default=True)
    soya = Column(Boolean, nullable=False, default=True)
    sulphites = Column(Boolean, nullable=False, default=True)
    vegan = Column(Boolean, nullable=False, default=True)
    vegetarian = Column(Boolean, nullable=False, default=True)


class Discount(Base):
    __tablename__ = "discounts"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    start_date = Column(Date)
    end_date = Column(Date)

    discount_multiplier = Column(Float)

    orders = relationship("Order", back_populates="discount")

    def __init__(self, name, start_date, end_date, discount_multiplier):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.discount_multiplier = discount_multiplier


class FoodCategory(Base):
    __tablename__ = "food_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String)

    menu_id = Column(Integer, ForeignKey("menus.id"))
    menu = relationship("Menu", back_populates="food_categories", uselist=False)

    recipes = relationship("Recipe", back_populates="food_category")

    def __init__(self, name, menu_id):
        self.name = name
        self.menu_id = menu_id


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True)

    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    restaurant = relationship("Restaurant", back_populates="inventory", uselist=False)

    stock_items = relationship("StockItem", back_populates="inventory")

    def __init__(self, restaurant_id):
        self.restaurant_id = restaurant_id


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String)

    food_categories = relationship("FoodCategory", back_populates="menu")

    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    restaurant = relationship("Restaurant", back_populates="menu", uselist=False)

    def __init__(self, name, restaurant_id):
        self.name = name
        self.restaurant_id = restaurant_id


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)

    date_placed = Column(Date)
    time_placed = Column(Time)

    ready_time = Column(Time)

    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    restaurant = relationship("Restaurant", back_populates="orders", uselist=False)

    discount_id = Column(Integer, ForeignKey("discounts.id"))
    discount = relationship("Discount", back_populates="orders")

    payment = relationship("Payment", back_populates="order", uselist=False)

    ready = Column(Boolean, nullable=False, default=False)

    order_recipes = relationship("OrderRecipe", back_populates="order")

    def __init__(self, table_id, discount_id, order_recipes):
        self.table_id = table_id
        self.discount_id = discount_id
        self.order_recipes = order_recipes
        dt = datetime.now()
        self.date_placed = datetime.date(dt)
        self.time_placed = datetime.time(dt)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)

    order_id = Column(Integer, ForeignKey("orders.id"))
    order = relationship("Order", back_populates="payment")

    price = Column(Float)
    final_price = Column(Float)

    def __init__(self, price, order_id):
        self.price = price
        self.order_id = order_id


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    available = Column(Boolean, nullable=False, default=True)

    food_category_id = Column(Integer, ForeignKey("food_categories.id"))
    food_category = relationship("FoodCategory", back_populates="recipes")

    recipe_items = relationship("RecipeItem", back_populates="recipe")

    order_recipes = relationship("OrderRecipe", back_populates="recipe")

    def __init__(self, name, description, price, food_category_id):
        self.name = name
        self.description = description
        self.price = price
        self.food_category_id = food_category_id


class RecipeItem(Base):
    __tablename__ = "recipe_items"

    id = Column(Integer, primary_key=True)

    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    recipe = relationship("Recipe", back_populates="recipe_items", uselist=False)

    stock_item_id = Column(Integer, ForeignKey("stock_items.id"))
    stock_item = relationship("StockItem", back_populates="recipe_items")

    quantity = Column(Integer, nullable=False)

    def __init__(self, recipe_id, stock_item_id, quantity):
        self.recipe_id = recipe_id
        self.quantity = quantity
        self.stock_item_id = stock_item_id


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, autoincrement=True)

    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    restaurant = relationship(
        "Restaurant", back_populates="reservations", uselist=False
    )

    name = Column(String)
    date = Column(Date)
    time = Column(Time)

    number_of_people = Column(Integer)

    table_id = Column(Integer, ForeignKey("tables.id"))
    table = relationship("Table", back_populates="reservations")

    def __init__(self, restaurant_id, name, date, time, number_of_people, table_id):
        self.restaurant_id = restaurant_id
        self.name = name
        self.date = date
        self.time = time
        self.number_of_people = number_of_people
        self.table_id = table_id


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False, unique=True)
    city = Column(String(100), nullable=False)

    capacity = Column(Integer, nullable=False)

    tables = relationship("Table", back_populates="restaurant")
    reservations = relationship("Reservation", back_populates="restaurant")
    orders = relationship("Order", back_populates="restaurant")

    inventory = relationship("Inventory", back_populates="restaurant", uselist=False)
    menu = relationship("Menu", back_populates="restaurant", uselist=False)

    def __init__(self, name, city, capacity):
        self.name = name
        self.city = city
        self.capacity = capacity
        self.inventory = Inventory(self.id)
        self.menu = Menu(f"Restaurant id {self.id} Menu", self.id)


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, autoincrement=True)
    capacity = Column(Integer)

    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    restaurant = relationship("Restaurant", back_populates="tables")

    reservations = relationship("Reservation", back_populates="table")

    def __init__(self, restaurant_id, capacity):
        self.restaurant_id = restaurant_id
        self.capacity = capacity


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String)

    back_end_staff = Column(Boolean)
    front_end_staff = Column(Boolean)
    delivery_staff = Column(Boolean)
    admin = Column(Boolean)

    accounts = relationship("Account", back_populates="role")

    def __init__(
        self,
        name,
        back_end_staff=False,
        front_end_staff=False,
        delivery_staff=False,
        admin=False,
    ):
        self.name = name
        self.back_end_staff = back_end_staff
        self.front_end_staff = front_end_staff
        self.delivery_staff = delivery_staff
        self.admin = admin


class StockItem(Base):
    __tablename__ = "stock_items"

    id = Column(Integer, primary_key=True)

    inventory_id = Column(Integer, ForeignKey("inventory.id"))
    inventory = relationship("Inventory", back_populates="stock_items", uselist=False)

    name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    re_order_quantity = Column(Integer, nullable=False)
    re_order_warning = Column(Boolean, nullable=False, default=False)

    dietary_requirements = relationship(
        "DietaryRequirement", back_populates="stock_item", uselist=False
    )

    recipe_items = relationship("RecipeItem", back_populates="stock_item")

    def __init__(
        self, inventory_id, name, quantity, re_order_quantity, dietary_requirements
    ):
        self.inventory_id = inventory_id
        self.name = name
        self.quantity = quantity
        self.re_order_quantity = re_order_quantity
        self.dietary_requirements = dietary_requirements


class OrderRecipe(Base):
    __tablename__ = "order_recipe"

    id = Column(Integer, primary_key=True, autoincrement=True)

    order_id = Column(Integer, ForeignKey("orders.id"))
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_recipes")
    recipe = relationship("Recipe", back_populates="order_recipes")

    def __init__(self, order_id, recipe_id, quantity):
        self.order_id = order_id
        self.recipe_id = recipe_id
        self.quantity = quantity
