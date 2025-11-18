from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Admin site customization
admin.site.site_header = "NGO Admin Panel"
admin.site.site_title = "NGO Admin"
admin.site.index_title = "Welcome to NGO Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ngo.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)