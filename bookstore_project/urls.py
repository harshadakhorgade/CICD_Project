
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bookstore.urls')),  # your app URLs
]

# Add this block at the bottom of this file
if settings.DEBUG:
   
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
