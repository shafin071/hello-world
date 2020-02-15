from django.urls import path

from .views import search_list_view

urlpatterns = [
    path('', search_list_view, name='search_list'),
]