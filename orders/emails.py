from django.core.mail import send_mail
from django.conf import settings


def send_order_confirmation_email(order):
    """Send a confirmation email to the customer after placing an order."""
    subject = f'Martify – Order Confirmation #{order.id}'
    items_lines = '\n'.join(
        f'  • {item.quantity} × {item.product.name}  (${item.price} each)'
        for item in order.items.all()
    )
    message = f"""Hi {order.first_name},

Thank you for your order at Martify! 🛒

──────────────────────────────
Order #{order.id}
──────────────────────────────
{items_lines}

Subtotal : ${order.subtotal}
Discount : -${order.discount_amount}
Total    : ${order.total}
──────────────────────────────

Shipping to:
{order.full_name}
{order.address}
{order.city}, {order.state} {order.zip_code}
{order.country}

We will notify you once your order is shipped.

Thanks for shopping with Martify!
"""
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
            fail_silently=False,
        )
    except Exception as e:
        # Log the error but don't crash the order process
        print(f"[Email Error] Could not send order confirmation: {e}")
