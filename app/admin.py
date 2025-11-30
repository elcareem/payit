# app/admin.py

from sqladmin import ModelView, Admin

from app.models.user import User
from app.models.product import Product
from app.models.buyer import Buyer
from app.models.farmer import Farmer
from app.models.order import Order
from app.models.product_category import ProductCategory

class UserAdmin(ModelView, model=User):
    name = "User"
    icon = "fa fa-user"

    column_list = ["id", "name", "email", "gender", "created_at"]
    form_excluded_columns = ["password", "created_at", "updated_at"]

    relationship_columns = [User.buyer, User.farmer]


class ProductAdmin(ModelView, model=Product):
    name = "Product"
    icon = "fa fa-box"

    column_list = [
        "id",
        "name",
        "price",
        "farmer.user.name",
        "category.name",
        "created_at",
    ]
    form_excluded_columns = ["created_at", "updated_at"]

    relationship_columns = [Product.orders]


class BuyerAdmin(ModelView, model=Buyer):
    name = "Buyer"
    icon = "fa fa-user-check"

    column_list = ["id", "user.name", "created_at"]
    form_excluded_columns = ["created_at", "updated_at"]

    relationship_columns = [Buyer.orders]


class FarmerAdmin(ModelView, model=Farmer):
    name = "Farmer"
    icon = "fa fa-tractor"

    column_list = ["id", "user.name", "created_at"]
    form_excluded_columns = ["created_at", "updated_at"]

    relationship_columns = [Farmer.products]


class OrderAdmin(ModelView, model=Order):
    name = "Order"
    icon = "fa fa-shopping-cart"

    column_list = [
        "id",
        "product.name",
        "buyer.user.name",
        "unit_price",
        "quantity",
        "amount",
        "status",
        "created_at",
    ]
    form_excluded_columns = ["created_at", "updated_at"]


class ProductCategoryAdmin(ModelView, model=ProductCategory):
    name = "Product Categorie"
    icon = "fa fa-tags"

    column_list = ["id", "name", "created_at"]
    form_excluded_columns = ["created_at", "updated_at"]

    relationship_columns = [ProductCategory.products]


def init_admin(app, engine):
    admin = Admin(app, engine)

    admin.add_view(UserAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(BuyerAdmin)
    admin.add_view(FarmerAdmin)
    admin.add_view(OrderAdmin)
    admin.add_view(ProductCategoryAdmin)

    return admin
