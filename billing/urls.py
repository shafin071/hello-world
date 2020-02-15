from django.urls import path

from .views import PaymentView

urlpatterns = [
    path('payment-method/', PaymentView.as_view(), name='payment-method'),
]