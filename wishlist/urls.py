from django.urls import path
from . import views

app_name = "wishlist"

urlpatterns = [
    # Page
    path("", views.wishlist_page, name="wishlist_page"),

    # Toggle (add if missing, remove if present)
    path("toggle/<int:product_id>/", views.wishlist_toggle, name="wishlist_toggle"),

    # Explicit remove a single product
    path("remove/<int:product_id>/", views.wishlist_remove, name="wishlist_remove"),

    # Clear entire wishlist
    path("clear/", views.wishlist_clear, name="wishlist_clear"),

    # Update / remove notes on a specific item
    path("notes/<int:item_id>/", views.wishlist_remove_note, name="wishlist_item_notes"),

    # Status check for a product (heart icon state)
    path("status/<int:product_id>/", views.wishlist_status, name="wishlist_status"),
]
