from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, HealthProfileViewSet, HealthIssueViewSet, ConsultationViewSet, FoodViewSet, HealthPlanViewSet


router = DefaultRouter()
router.register("users", UserViewSet)
router.register("health-profiles", HealthProfileViewSet)
router.register("health-issues", HealthIssueViewSet)
router.register("consultations", ConsultationViewSet)
router.register("foods", FoodViewSet)
router.register("health-plans", HealthPlanViewSet)

urlpatterns = [
    path("", include(router.urls)),
]