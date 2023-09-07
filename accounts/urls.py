from django.urls import path
from . import views

urlpatterns = [
    path('signup/<str:user_type>/', view=views.SignUpView.as_view(), name='signup'),
    path('login/<str:user_type>/', view=views.LoginView.as_view(), name='login')
]
