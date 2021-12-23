from django.urls import re_path
from django.conf.urls import include

from team import views

from rest_framework.routers import DefaultRouter
# 'base_name' is optional. Needed only if the same viewset is registered more than once
# Official DRF docs on this option: http://www.django-rest-framework.org/api-guide/routers/

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.

router = DefaultRouter()
router.register(r'team', views.TeamViewSet)

urlpatterns = [
    re_path(r'', include(router.urls)),
]