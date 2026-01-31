from django.urls import path
from . import views

urlpatterns = [
    path("wishlist/", views.wishlist_page, name="wishlist_page"),
    path("wishlist/toggle/<int:product_id>/",
         views.wishlist_toggle, name="wishlist_toggle"),
    path("wishlist/status/<int:product_id>/",
         views.wishlist_status, name="wishlist_status"),
]
