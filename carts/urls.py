from django.urls import path

from .views import CartHomeView, CartUpdateView, CartRefreshAPIView, CheckoutHome, CheckoutDoneView

urlpatterns = [

    path('', CartHomeView.as_view(), name='home'),
    path('update/', CartUpdateView.as_view(), name='update'),
    path('refresh-cart/', CartRefreshAPIView.as_view(), name='refresh-cart'),
    path('checkout/', CheckoutHome.as_view(), name='checkout'),
    path('checkout/success/', CheckoutDoneView.as_view(), name='success'),

]
