from .models import Category
from cart.cart import SessionCart


def search_category(request):
    categories = Category.objects.all()
    return dict(categories=categories)


def cart_context(request):
    """
    Make the cart available globally in templates.
    """
    cart = SessionCart(request)
    return {'cart': cart}
