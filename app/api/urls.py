from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from api import views
from .views import UserViewSet, CategoryViewSet, GenreViewSet, \
    TitleViewSet, ReviewViewSet, CommentViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>[0-9]+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet, basename='comments')

urlpatterns = [
    path('auth/email/', views.ObtainEmailAPIView.as_view()),
    path('auth/token/', views.EmailAuthAPIView.as_view(), name='token_obtain'),
    path('auth/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('', include(router.urls)),
]
