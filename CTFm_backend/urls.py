from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include('challenge.urls')),
    path('api/v1/',include('user.urls')),
    path('api/v1/',include('notification.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
