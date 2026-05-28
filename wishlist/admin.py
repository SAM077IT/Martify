from django.contrib import admin
from .models import Wishlist, WishlistItem


class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 0
    readonly_fields = ("created_at", "updated_at")


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "item_count", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("created_at", "updated_at")
    inlines = [WishlistItemInline]

    @admin.display(description="Items")
    def item_count(self, obj):
        return obj.items.count()


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ("product", "wishlist_user", "has_notes", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at", "product__category")
    search_fields = ("product__name", "wishlist__user__username", "notes")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("wishlist",)
    actions = ["remove_selected_items", "clear_notes"]

    @admin.display(description="User")
    def wishlist_user(self, obj):
        return obj.wishlist.user.username

    @admin.display(description="Notes", boolean=True)
    def has_notes(self, obj):
        return bool(obj.notes)

    @admin.action(description="Remove selected items from wishlists")
    def remove_selected_items(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} item(s) removed from wishlists.")

    @admin.action(description="Clear notes on selected items")
    def clear_notes(self, request, queryset):
        updated = queryset.update(notes="")
        self.message_user(request, f"Notes cleared on {updated} item(s).")
