from django.urls import path
from .views import IndexView, ShopView, CategoryView, ProductView, ContactUs, AboutUs

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('contact/', ContactUs.as_view(), name="contact"),
    path('about/', AboutUs.as_view(), name="about"),
    path('shop/', ShopView.as_view(), name="shop"),
    path('shop/category/<str:category>',
         CategoryView.as_view(), name="shop_with_category"),
    path('shop/product/<str:product>',
         ProductView.as_view(), name="shop_product"),
]
