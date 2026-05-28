from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import transaction
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
            'country': 'US',  # Default country selection
        })
        return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})

    def post(self, request):
        cart = SessionCart(request)
        if len(cart) == 0:
            messages.warning(request, 'Your cart is empty.')
            return redirect('cart_detail')

        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Extract payment details from POST data
            payment_method = request.POST.get('payment_method', 'cod')
            payment_extra_charge = request.POST.get(
                'payment_extra_charge', '0.00')
            payment_app = request.POST.get('payment_app', '')

            # Determine the user for this order
            order_user = None
            created_user = None

            try:
                with transaction.atomic():
                    if request.user.is_authenticated:
                        # Logged in user - use the existing user
                        order_user = request.user
                    else:
                        create_account = request.POST.get(
                            'create_account', '0') == '1'
                        if create_account:
                            # Create a new user account
                            password = form.cleaned_data.get(
                                'account_password')
                            if not password:
                                form.add_error(
                                    'account_password', 'Password is required to create an account.')
                                return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})

                            # Generate a username from email (first part before @)
                            email = form.cleaned_data.get('email')
                            base_username = email.split('@')[0][:30]
                            username = base_username
                            counter = 1
                            while User.objects.filter(username=username).exists():
                                username = f"{base_username}_{counter}"
                                counter += 1

                            created_user = User.objects.create_user(
                                username=username,
                                email=email,
                                password=password,
                                first_name=form.cleaned_data.get(
                                    'first_name', ''),
                                last_name=form.cleaned_data.get(
                                    'last_name', ''),
                            )
                            order_user = created_user

                            # Auto-login the newly created user
                            auth_user = authenticate(
                                request,
                                username=username,
                                password=password,
                            )
                            if auth_user:
                                login(request, auth_user)
                        else:
                            # Guest user - order_user stays None
                            pass

                    # Create the order
                    order = form.save(commit=False)
                    if order_user:
                        order.user = order_user
                    if cart.coupon:
                        order.coupon = cart.coupon
                        order.discount = cart.coupon.discount

                    # Save payment details to order
                    order.payment_method = payment_method
                    if payment_method == 'cod':
                        order.stripe_payment_intent = ''  # No payment intent for COD
                    elif payment_method == 'card':
                        # Card payments would be processed separately
                        pass
                    elif payment_method == 'apps' and payment_app:
                        order.stripe_payment_intent = f"app_{payment_app}"

                    order.save()

                    # Create order items from cart
                    for item in cart:
                        OrderItem.objects.create(
                            order=order,
                            product=item['product'],
                            price=item['price'],
                            quantity=item['quantity'],
                        )

                    # Clear cart
                    cart.clear()

                    # Store order id in session for the thank you page
                    request.session['order_id'] = order.id

                    # Send confirmation email
                    send_order_confirmation_email(order)

                    messages.success(
                        request, f'Order #{order.id} placed successfully!')
                    return redirect('order_thankyou')

            except Exception as e:
                messages.error(
                    request, f'An error occurred while placing your order: {str(e)}')
                return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})

        return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})


class ThankYouView(View):
    """Display order confirmation / thank you page."""

    def get(self, request):
        order_id = request.session.get('order_id')
        if not order_id:
            messages.warning(request, 'No recent order found.')
            return redirect('index')

        order = get_object_or_404(Order, id=order_id)

        # If the order belongs to a user, verify it's the current user
        if order.user and request.user.is_authenticated and order.user != request.user:
            messages.warning(request, 'You do not have access to this order.')
            return redirect('index')

        # Clear the session order_id so the page doesn't get re-shown
        del request.session['order_id']

        return render(request, 'orders/thankyou.html', {'order': order})


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
