from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, MenuItemViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'menu-items', MenuItemViewSet, basename='menuitem')

urlpatterns = router.urls
