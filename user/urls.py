from django.urls import path
from django.conf.urls import include, url

from user import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

from rest_framework.routers import DefaultRouter
# 'base_name' is optional. Needed only if the same viewset is registered more than once
# Official DRF docs on this option: http://www.django-rest-framework.org/api-guide/routers/

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.

router = DefaultRouter()
router.register(r'user', views.UserViewSet)

urlpatterns = [
    path('auth/register/', views.register),
    path('auth/obtainToken/', views.obtainToken,name="token_obtain"),
    path('auth/refreshToken/', TokenRefreshView.as_view(),name="token_refresh"),
    path('auth/verifyToken/',TokenVerifyView.as_view(), name='token_verify'),
    url(r'^', include(router.urls)),
]