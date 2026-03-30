from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from .models import Coupon
from .forms import CouponApplyForm


@require_POST
def coupon_apply(request):
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        now = timezone.now()
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True,
            )
            request.session['coupon_id'] = coupon.id
            messages.success(request, f'Coupon "{coupon.code}" applied! {coupon.discount}% off.')
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            messages.error(request, 'Invalid or expired coupon code.')
    return redirect('cart_detail')
