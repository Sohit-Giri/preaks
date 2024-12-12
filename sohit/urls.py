from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from sohit import settings

urlpatterns = [
    path('redbull/', admin.site.urls),
    path('', include('myapp.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)