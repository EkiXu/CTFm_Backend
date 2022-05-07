from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from notification import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'notification', views.NotificationViewSet)
router.register(r'admin/notification', views.AdminNotificationViewSet)

# 'base_name' is optional. Needed only if the same viewset is registered more than once
# Official DRF docs on this option: http://www.django-rest-framework.org/api-guide/routers/

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    re_path(r'', include(router.urls)),
]