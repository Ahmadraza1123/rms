from rest_framework.routers import DefaultRouter
from .views import DishReviewViewSet, ServiceReviewViewSet

router = DefaultRouter()
router.register(r'dish-reviews', DishReviewViewSet, basename='dishreview')
router.register(r'service-reviews', ServiceReviewViewSet, basename='servicereview')

urlpatterns = router.urls
