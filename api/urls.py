from django.urls import path
from .views import UserView,SpecificUserView,InterestsView,CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('users/',UserView.as_view(),name='user'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('interests/',InterestsView.as_view(),name='interests'),
    path('interests/<int:pk>',InterestsView.as_view(),name='interests'),
    path('users/<int:pk>',SpecificUserView.as_view(),name='user')
]
