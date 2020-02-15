from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (StudentProfileDetailView,
                    ChangeNameView,
                    change_password,
                    AvatarChangeView,
                    AboutMeChangeView,
                    AddressUpdateView,
                    AccountDeleteConfirmView,
                    AccountDeleteView,
                    PurchaseHistoryView,
                    register_page,
                    login_page
                    )


from . import views

urlpatterns = [
    path('profile/<slug:slug>', StudentProfileDetailView.as_view(), name='student_profile_view'),
    path('change-name/<slug:slug>', ChangeNameView.as_view(), name='edit_profile'),
    path('change-password/', change_password, name='change_password'),
    path('upload/', AvatarChangeView.as_view(), name='upload_photo'),
    path('about-me/', AboutMeChangeView.as_view(), name='about_me'),
    path('change-address/', AddressUpdateView.as_view(), name='change_address'),
    path('delete-account-confirm/', AccountDeleteConfirmView.as_view(), name='delete_account_confirm'),
    path('delete-account/<pk>', AccountDeleteView.as_view(), name='delete_account'),
    path('purchase-history', PurchaseHistoryView.as_view(), name='purchase_history'),
    path('register/', register_page, name='register_page'),
    path('login/', login_page, name='login'),                 # Navbar login
    path('logout/', LogoutView.as_view(), name='logout'),




]



