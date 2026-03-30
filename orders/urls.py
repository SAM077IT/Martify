from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('history/', views.OrderHistoryView.as_view(), name='order_history'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
]
