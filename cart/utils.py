"""
Cart utilities for synchronizing session cart with database cart.
"""
from decimal import Decimal
from django.conf import settings
from core.models import Product
from .models import Cart, CartItem
from .cart import SessionCart


def sync_cart_to_db(user, session_cart):
    """
    Synchronize the database cart to exactly match the session cart.

    This function REPLACES the user's database cart contents with the items
    from the session cart. It ensures the DB is an exact mirror of the session.

    Args:
        user: The authenticated user
        session_cart: SessionCart instance

    Returns:
        Cart instance if cart has items, None if cart is empty (and DB cart deleted)
    """
    # If session cart is empty, delete DB cart and return None
    if len(session_cart) == 0:
        Cart.objects.filter(user=user).delete()
        return None

    # Get or create the user's cart
    db_cart, created = Cart.objects.get_or_create(user=user)

    # Delete all existing items in the DB cart
    db_cart.items.all().delete()

    # Create new items from session cart
    for item_data in session_cart:
        product = item_data['product']
        quantity = item_data['quantity']
        if quantity > 0:
            CartItem.objects.create(cart=db_cart, product=product, quantity=quantity)

    return db_cart


def load_db_cart_into_session(user, session_cart):
    """
    Load a user's database cart into the session cart, merging with any existing session items.

    Args:
        user: The authenticated user
        session_cart: SessionCart instance

    Returns:
        bool: True if DB cart was loaded, False if no DB cart exists
    """
    try:
        db_cart = Cart.objects.get(user=user)

        # Add each DB cart item to session cart
        for db_item in db_cart.items.all():
            session_cart.add(
                product=db_item.product,
                quantity=db_item.quantity,
                override_quantity=False
            )

        return True
    except Cart.DoesNotExist:
        return False


def clear_user_db_cart(user):
    """Remove all items from user's database cart."""
    try:
        db_cart = Cart.objects.get(user=user)
        db_cart.delete()
    except Cart.DoesNotExist:
        pass
