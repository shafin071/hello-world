from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path


from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home_page'),
    path('billing/', include(('billing.urls', 'billing'), namespace='billing')),
    path('contact/', include(('contactUs.urls', 'contact'), namespace='contact')),
    path('students/', include(('students.urls', 'students'), namespace='students')),
    path('instructors/', include(('instructors.urls', 'instructors'), namespace='instructors')),
    path('courses/', include(('courses.urls', 'courses'), namespace='courses')),
    path('search/', include(('search.urls', 'search'), namespace='search')),
    path('cart/', include(('carts.urls', 'cart'), namespace='cart')),
    path('address/', include(('addresses.urls', 'addresses'), namespace='addresses')),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'),
         name='password_reset_complete'),

]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)