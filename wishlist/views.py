from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from .models import Wishlist, WishlistItem
from core.models import Product


def _get_or_create_wishlist(user):
    wishlist, _ = Wishlist.objects.get_or_create(user=user)
    return wishlist


@login_required
@require_POST
def wishlist_toggle(request, product_id):
    """
    AJAX endpoint:
    - If product is not in wishlist -> add it
    - If product is in wishlist -> remove it
    Returns JSON: {added: bool, in_wishlist: bool, wishlist_count: int}
    """
    product = get_object_or_404(Product, pk=product_id)
    print(product)
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
            # Rare race condition protection (double-click, simultaneous requests)
            added = False
            in_wishlist = True

    wishlist_count = wishlist.items.count()
    return JsonResponse(
        {
            "added": added,
            "in_wishlist": in_wishlist,
            "wishlist_count": wishlist_count,
            "product_id": product.id,
        }
    )


@login_required
def wishlist_page(request):
    """
    Page where logged-in user can view their wishlist.
    """
    wishlist = _get_or_create_wishlist(request.user)
    # Prefetch products for fewer queries
    items = (
        wishlist.items.select_related("product")
        .order_by("-created_at")
    )
    return render(
        request,
        "wishlist.html",
        {"items": items},
    )


@login_required
def wishlist_status(request, product_id):
    """
    Optional: handy for product page initial state (heart filled/unfilled).
    Returns JSON: {in_wishlist: bool}
    """
    wishlist = _get_or_create_wishlist(request.user)
    in_wishlist = wishlist.items.filter(product_id=product_id).exists()
    return JsonResponse({"in_wishlist": in_wishlist, "product_id": product_id})
