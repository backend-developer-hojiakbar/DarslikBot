from django.urls import path, include
from .views import RegisterView, VerifyUserEmail, OneTimePasswordViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('code', OneTimePasswordViewSet, basename='code')
urlpatterns = [
    path('', include(router.urls)),
    path('users/', RegisterView.as_view(),),
    path('verify-email', VerifyUserEmail.as_view(),),
]