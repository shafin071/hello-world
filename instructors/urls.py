from django.urls import path

from .views import InstructorListView, InstructorDetailView

urlpatterns = [

    path('', InstructorListView.as_view(), name='instructor_list'),
    path('<slug:slug>/', InstructorDetailView.as_view(), name='instructor_profile'),
]