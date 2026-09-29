from rest_framework.routers import DefaultRouter
from .views_sequence import SequenceViewSet
router = DefaultRouter()
router.register('', SequenceViewSet, basename='sequence')
urlpatterns = router.urls
