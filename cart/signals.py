"""
Signal handlers for cart synchronization with authentication events.
"""
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .cart import SessionCart
from .utils import sync_cart_to_db, load_db_cart_into_session


@receiver(user_logged_in)
def on_login(sender, request, user, **kwargs):
    """
    Synchronize cart when user logs in.

    Steps:
    1. Load the user's existing DB cart (if any) into the session cart.
       This merges DB items with any guest items already in session.
    2. Synchronize the DB cart to match the combined session cart.
    3. Clear the session cart and reload from DB to ensure consistency.
    """
    session_cart = SessionCart(request)

    # Step 1: Load existing DB cart into session, merging with any guest items
    load_db_cart_into_session(user, session_cart)

    # Step 2: Sync DB cart to match the current session cart (combined)
    sync_cart_to_db(user, session_cart)

    # Step 3: Clear and reload from DB to ensure session reflects authoritative DB state
    session_cart.clear()
    load_db_cart_into_session(user, session_cart)


@receiver(user_logged_out)
def on_logout(sender, request, user, **kwargs):
    """
    Handle logout event.

    Note: Cart is already synchronized during the session via per-operation sync,
    so no additional database persistence is needed here.
    Django's logout() flushes the session automatically.
    """
    # No action required; DB cart is up to date.
    pass
