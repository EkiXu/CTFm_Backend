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
router.register(r'admin/user', views.AdminUserViewSet)

urlpatterns = [
    path('auth/register/', views.register),
    path('auth/obtain_token/', views.obtainToken,name="token_obtain"),
    path('auth/refresh_token/', TokenRefreshView.as_view(),name="token_refresh"),
    path('auth/verify_token/',TokenVerifyView.as_view(), name='token_verify'),
    path('auth/reset_password_email/',views.resetPasswordRequest, name='reset_password_email'),
    url(r'^auth/activate/(?P<user_id>\d+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
        views.activate, name='activate'),
    url(r'^auth/reset_password/(?P<user_id>\d+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
        views.resetPassword, name='activate'),
    url(r'', include(router.urls)),
]