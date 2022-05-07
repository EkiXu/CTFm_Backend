from django.urls import include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import ExtendedSimpleRouter

from challenge import views

# Create a router and register our viewsets with it.
router = ExtendedSimpleRouter()
(
    router.register(r'category', views.ChallengeCategoryViewSet,basename='category')
          .register(r'challenge', views.CategoryChallengeViewset, basename='category-challenges',parents_query_lookups=['category_id'])
)
router.register(r'challenge', views.ChallengeViewSet)
router.register(r'admin/category', views.AdminChallengeCategoryViewSet)
router.register(r'admin/challenge', views.AdminChallengeViewSet)



# 'base_name' is optional. Needed only if the same viewset is registered more than once
# Official DRF docs on this option: http://www.django-rest-framework.org/api-guide/routers/

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    re_path(r'', include(router.urls)),
]