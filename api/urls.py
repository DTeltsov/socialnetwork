from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework import routers

from .views import PostViewSet, PostRateViewSet, UserViewSet, UserActivityViewSet

router = routers.DefaultRouter()
router.register(r'post',PostViewSet)
router.register(r'postrate',PostRateViewSet)
router.register(r'user', UserViewSet)
router.register(r'activity', UserActivityViewSet)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('', include(router.urls))
]
