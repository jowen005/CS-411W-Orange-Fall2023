from django.urls import path
from . import views

urlpatterns = [
    path('handshake/', views.handshake, name='handshake'),
]