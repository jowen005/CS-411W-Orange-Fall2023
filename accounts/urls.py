from django.urls import path
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from . import views


urlpatterns = [
    path('signup/<str:user_type>/', view=views.SignUpView.as_view(), name='signup'),
    path('login/', view=views.LoginView.as_view(), name='login'),
    path('jwt/create/', TokenObtainPairView.as_view(), name='jwt_create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt_verify'),
]

