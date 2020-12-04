from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from notification import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'notification', views.NotificationViewSet)

# 'base_name' is optional. Needed only if the same viewset is registered more than once
# Official DRF docs on this option: http://www.django-rest-framework.org/api-guide/routers/

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]