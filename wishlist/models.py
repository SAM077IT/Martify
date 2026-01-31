from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Wishlist(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="wishlist",
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"Wishlist({self.user_id})"


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        "core.Product",
        on_delete=models.CASCADE,
        related_name="wishlisted_in",
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["wishlist", "product"],
                name="uniq_wishlist_product",
            )
        ]

    def __str__(self) -> str:
        return f"WishlistItem(wishlist={self.wishlist_id}, product={self.product_id})"
