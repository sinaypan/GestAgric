from django.urls import path
from . import views

urlpatterns = [
    path('centres/', views.centre_list, name='centre_list'),
    path('centre/new/', views.centre_new, name='centre_new'),
    path('centre/<int:pk>/', views.centre_detail, name='centre_detail'),
    path('centre/<int:pk>/edit/', views.centre_edit, name='centre_edit'),
    path('centre/<int:pk>/delete/', views.centre_delete, name='centre_delete'),

    path('employes/', views.employe_list, name='employe_list'),
    path('employe/new/', views.employe_new, name='employe_new'),
    path('employe/<int:pk>/', views.employe_detail, name='employe_detail'),
    path('employe/<int:pk>/edit/', views.employe_edit, name='employe_edit'),
    path('employe/<int:pk>/delete/', views.employe_delete, name='employe_delete'),
]
