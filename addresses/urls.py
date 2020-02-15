from django.urls import path

from .views import CheckoutAddressCreateView, CheckoutAddressReuseView

urlpatterns = [
    path('checkout/address/create/', CheckoutAddressCreateView.as_view(), name='checkout_address_create'),
    path('checkout/address/reuse/', CheckoutAddressReuseView.as_view(), name='checkout_address_reuse'),
]