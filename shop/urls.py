from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("clothes/", views.clothes, name="clothes"),
    path("accessories/", views.accessories, name="accessories"),
    path("cart/<int:id>/", views.cart, name="cart"),
    path("cartadd/<int:item_id>", views.AddToCart, name="add_to_cart"),
    path("delete/<int:item_id>", views.DeleteItem, name="delete_item"),
    path("login/", views.userlogin, name="login"),
    path("send_email/", views.send_email, name="send_email"),
    path("search/", views.search, name="search"),
    path("register/", views.register, name="register"),
    path("logout/", views.userLogout, name="logout"),
]
