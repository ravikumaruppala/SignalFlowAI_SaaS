from rest_framework.routers import DefaultRouter
from .views import InboxReplyViewSet
router = DefaultRouter(); router.register('', InboxReplyViewSet, basename='inbox')
urlpatterns = router.urls
