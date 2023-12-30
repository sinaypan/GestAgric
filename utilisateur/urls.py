from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('clients/', views.client_list, name='client_list'),
    path('client/<int:pk>/', views.client_detail, name='client_detail'),
    path('client/new/', views.client_new, name='client_new'),
    path('client/<int:pk>/edit/', views.client_edit, name='client_edit'),
    path('client/<int:pk>/delete/', views.client_delete, name='client_delete'),
    
    path('authentification/login_user', views.login_user, name="login"),
    path('authentification/logout_user', views.logout_user, name='logout'),
    path('authentification/register_user', views.register_user, name='register_user'),
]

