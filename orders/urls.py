from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("create/<int:book_id>/", views.create_order, name="create_order"),
    path("success/<int:order_id>/", views.order_success, name="order_success"),

    path("cart_detail/", views.cart_detail, name="cart_detail"),
    path("cart/<int:book_id>/", views.add_cart, name="cart"),

    path("cart/delete/<int:book_id>/", views.delete_cart, name="delete_cart"),
    path("cart/delete-all/", views.delete_all_cart, name="delete_all_cart"),
]


