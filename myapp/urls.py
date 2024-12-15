from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from sohit import settings
from . import views
# myapp/urls.py
from django.urls import path
from . import views
from django.conf.urls import handler404

from myapp.views import custom_404  # Replace 'your_app' with the actual app name

handler404 = 'myapp.views.custom_404'
urlpatterns = [
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('validate-email/', views.validate_email, name='validate_email'),
    path('guest-login/', views.guest_login, name='guest_login'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
