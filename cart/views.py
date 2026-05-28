from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from core.models import Product
from .cart import SessionCart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from .utils import sync_cart_to_db


def cart_detail(request):
    cart = SessionCart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True}
        )
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/cart.html', {
        'cart': cart,
        'coupon_apply_form': coupon_apply_form,
    })


@require_POST
def cart_add(request, product_id):
    cart = SessionCart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
        # Sync to database for logged-in users
        if request.user.is_authenticated:
            sync_cart_to_db(request.user, cart)

    # AJAX support
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart_total = Decimal(str(cart.total_price)).quantize(Decimal('0.01'))
        cart_discount = Decimal(str(cart.discount)).quantize(Decimal('0.01'))
        cart_total_after_discount = Decimal(str(cart.total_after_discount)).quantize(Decimal('0.01'))
        if form.is_valid():
            return JsonResponse({
                'success': True,
                'cart_count': len(cart),
                'cart_total': str(cart_total),
                'cart_discount': str(cart_discount),
                'cart_total_after_discount': str(cart_total_after_discount),
                'message': 'Product added to cart!',
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors.get('quantity', ['Invalid quantity.']),
                'cart_count': len(cart),
                'cart_total': str(cart_total),
                'cart_discount': str(cart_discount),
                'cart_total_after_discount': str(cart_total_after_discount),
            }, status=400)

    return redirect('cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = SessionCart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    # Sync to database for logged-in users
    if request.user.is_authenticated:
        sync_cart_to_db(request.user, cart)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart_total = Decimal(str(cart.total_price)).quantize(Decimal('0.01'))
        cart_discount = Decimal(str(cart.discount)).quantize(Decimal('0.01'))
        cart_total_after_discount = Decimal(str(cart.total_after_discount)).quantize(Decimal('0.01'))
        return JsonResponse({
            'cart_count': len(cart),
            'cart_total': str(cart_total),
            'cart_discount': str(cart_discount),
            'cart_total_after_discount': str(cart_total_after_discount),
            'message': 'Removed from cart.',
        })

    return redirect('cart_detail')


def cart_clear(request):
    cart = SessionCart(request)
    cart.clear()
    # Sync to database for logged-in users (will delete DB cart if empty)
    if request.user.is_authenticated:
        sync_cart_to_db(request.user, cart)
    return redirect('cart_detail')
