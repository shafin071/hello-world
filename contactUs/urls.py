from django.urls import path

from . import views

urlpatterns = [

    # path('', views.contact_page, name='contactUs'),
    path('', views.SignUpView.as_view(), name='signup'),
    path('signup-post/', views.SignUpPostView.as_view(), name='signup_post'),

]