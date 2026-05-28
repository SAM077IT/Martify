from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Wishlist, WishlistItem
from core.models import Product


def _get_or_create_wishlist(user):
    wishlist, _ = Wishlist.objects.get_or_create(user=user)
    return wishlist


@login_required
@require_POST
def wishlist_toggle(request: HttpRequest, product_id: int):
    """
    AJAX endpoint that toggles a product in/out of the user's wishlist.

    Response JSON:
        added        (bool) – True if added, False if removed
        in_wishlist  (bool) – Current state after toggle
        wishlist_count (int) – Total items in wishlist
        product_id   (int)  – The product that was toggled
    """
    product = get_object_or_404(Product, pk=product_id)
    wishlist = _get_or_create_wishlist(request.user)

    existing = WishlistItem.objects.filter(wishlist=wishlist, product=product)
    if existing.exists():
        existing.delete()
        added = False
        in_wishlist = False
    else:
        try:
            WishlistItem.objects.create(wishlist=wishlist, product=product)
            added = True
            in_wishlist = True
        except IntegrityError:
            # Race condition guard (double-click / simultaneous requests)
            added = False
            in_wishlist = True

    return JsonResponse(
        {
            "added": added,
            "in_wishlist": in_wishlist,
            "wishlist_count": WishlistItem.objects.filter(wishlist=wishlist).count(),
            "product_id": product.id,
        }
    )


@login_required
@require_POST
def wishlist_remove(request: HttpRequest, product_id: int):
    """
    AJAX endpoint to explicitly remove a product from the wishlist.
    Idempotent – returns success even if the item wasn't in the wishlist.

    Response JSON:
        removed       (bool) – True if an item was deleted
        wishlist_count (int) – Updated total items in wishlist
        product_id    (int)  – The product that was removed
    """
    product = get_object_or_404(Product, pk=product_id)
    wishlist = _get_or_create_wishlist(request.user)

    deleted_count, _ = WishlistItem.objects.filter(
        wishlist=wishlist, product=product
    ).delete()

    return JsonResponse(
        {
            "removed": deleted_count > 0,
            "wishlist_count": WishlistItem.objects.filter(wishlist=wishlist).count(),
            "product_id": product.id,
        }
    )


@login_required
@require_POST
def wishlist_clear(request: HttpRequest):
    """
    AJAX endpoint to remove ALL products from the user's wishlist.

    Response JSON:
        cleared    (bool) – Always True
        removed_count (int) – Number of items that were removed
    """
    wishlist = _get_or_create_wishlist(request.user)
    removed_count = wishlist.items.count()
    wishlist.clear()

    return JsonResponse(
        {
            "cleared": True,
            "removed_count": removed_count,
        }
    )


@login_required
@require_POST
def wishlist_remove_note(request: HttpRequest, item_id: int):
    """
    AJAX endpoint to clear/update the personal note on a wishlist item.
    POST body may contain "notes" field.

    Response JSON:
        notes (str) – The updated notes value
    """
    wishlist = _get_or_create_wishlist(request.user)
    item = get_object_or_404(WishlistItem, pk=item_id, wishlist=wishlist)
    notes = request.POST.get("notes", "").strip()
    item.update_notes(notes)

    return JsonResponse({"notes": item.notes, "item_id": item.id})


@login_required
def wishlist_page(request: HttpRequest):
    """\    Renders the wishlist page with all items for the logged-in user.
    """
    wishlist = _get_or_create_wishlist(request.user)
    items = (
        wishlist.items.select_related("product__category")
        .order_by("-created_at")
    )
    return render(
        request,
        "wishlist.html",
        {
            "wishlist": wishlist,
            "items": items,
            "items_count": items.count(),
        },
    )


@login_required
def wishlist_status(request: HttpRequest, product_id: int):
    """
    Returns the wishlist status for a specific product.
    Handy for initial heart icon state on the product detail page.

    Response JSON:
        in_wishlist (bool)
        product_id  (int)
    """
    wishlist = _get_or_create_wishlist(request.user)
    in_wishlist = wishlist.items.filter(product_id=product_id).exists()
    return JsonResponse({"in_wishlist": in_wishlist, "product_id": product_id})
