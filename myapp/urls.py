from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from sohit import settings
from . import views
# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('validate-email/', views.validate_email, name='validate_email'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
