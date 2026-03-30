"""
cart/cart.py  –  Session-based cart (works for guests + logged-in users).

For logged-in users, changes are also mirrored to the DB Cart model.
"""
from decimal import Decimal
from django.conf import settings
from core.models import Product
from coupons.models import Coupon


class SessionCart:
    """
    Stores cart data in request.session[CART_SESSION_ID].
    Structure:
        {
          "<product_id>": {
              "quantity": <int>,
              "price": "<str decimal>"
          },
          ...
        }
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # Coupon
        self.coupon_id = self.session.get('coupon_id')

    # ── internal helpers ──────────────────────────────────────────────────────

    def save(self):
        self.session.modified = True

    # ── public API ────────────────────────────────────────────────────────────

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.pop('coupon_id', None)
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    @property
    def total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    @property
    def discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.total_price
        return Decimal(0)

    @property
    def total_after_discount(self):
        return self.total_price - self.discount
