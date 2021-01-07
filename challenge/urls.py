from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from challenge import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'category', views.ChallengeCategoryViewSet)
router.register(r'challenge', views.ChallengeViewSet)
router.register(r'admin/category', views.AdminChallengeCategoryViewSet)
router.register(r'admin/challenge', views.AdminChallengeViewSet)


challenge_router = routers.NestedSimpleRouter(router, r'category', lookup='category')
challenge_router.register(r'challenge', views.CategoryChallengeViewset, basename='category-challenges')

# 'base_name' is optional. Needed only if the same viewset is registered more than once
# Official DRF docs on this option: http://www.django-rest-framework.org/api-guide/routers/

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'', include(router.urls)),
    url(r'', include(challenge_router.urls)),
]