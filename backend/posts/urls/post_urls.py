from rest_framework.routers import DefaultRouter

from posts.viewsets.post_viewset import PostViewSet

router = DefaultRouter()

router.register(
    '',
    PostViewSet,
    basename='posts',
)

urlpatterns = router.urls
