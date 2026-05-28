from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Wishlist(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="wishlist",
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"Wishlist(user={self.user.username}, items={self.items.count()})"

    @property
    def item_count(self) -> int:
        return self.items.count()

    def clear(self):
        """Remove all items from the wishlist."""
        self.items.all().delete()


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
    notes = models.TextField(
        blank=True,
        default="",
        help_text="Optional personal note about this wishlist item.",
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["wishlist", "product"],
                name="uniq_wishlist_product",
            )
        ]

    def __str__(self) -> str:
        return f"{self.product.name} in {self.wishlist.user.username}'s wishlist"

    def remove(self):
        """Remove this item from the wishlist."""
        self.delete()

    def update_notes(self, notes: str):
        """Update the personal note for this wishlist item."""
        self.notes = notes
        self.save(update_fields=["notes", "updated_at"])

    @property
    def is_in_stock(self) -> bool:
        """Check if the product is available (placeholder for stock logic)."""
        return True
