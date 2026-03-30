from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView
from django.contrib import messages
from cart.cart import SessionCart
from coupons.models import Coupon
from .models import Order, OrderItem
from .forms import OrderCreateForm
from .emails import send_order_confirmation_email


class CheckoutView(View):
    """Display checkout form and create order on POST."""

    def get(self, request):
        cart = SessionCart(request)
        if len(cart) == 0:
            messages.warning(request, 'Your cart is empty.')
            return redirect('cart_detail')

        form = OrderCreateForm(initial={
            'email': request.user.email if request.user.is_authenticated else '',
            'first_name': request.user.first_name if request.user.is_authenticated else '',
            'last_name': request.user.last_name if request.user.is_authenticated else '',
        })
        return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})

    def post(self, request):
        cart = SessionCart(request)
        if len(cart) == 0:
            messages.warning(request, 'Your cart is empty.')
            return redirect('cart_detail')

        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()

            # Create order items from cart
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )

            # Send confirmation email
            send_order_confirmation_email(order)

            # Clear cart
            cart.clear()

            # Store order id in session for payment
            request.session['order_id'] = order.id

            messages.success(request, f'Order #{order.id} placed successfully!')
            return redirect('payment_process', order_id=order.id)

        return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})


class OrderHistoryView(LoginRequiredMixin, ListView):
    """Show all orders for the logged-in user."""
    template_name = 'orders/order_history.html'
    context_object_name = 'orders'
    login_url = '/login/'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')


class OrderDetailView(LoginRequiredMixin, DetailView):
    """Show details for a specific order."""
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    login_url = '/login/'

    def get_queryset(self):
        # Users can only see their own orders
        return Order.objects.filter(user=self.request.user)
