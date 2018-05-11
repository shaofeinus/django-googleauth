from django.urls import path

from . import views

urlpatterns = [
    path('auth/', views.auth, name='googleauth-auth'),
    path('auth-redirect/', views.auth_redirect, name='googleauth-auth-redirect'),
    path('auth-success/', views.auth_success, name='googleauth-auth-success'),
    path('auth-error/', views.auth_error, name='googleauth-auth-error'),
]
