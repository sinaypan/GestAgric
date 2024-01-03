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

    path('gestion_employes/', views.gestion_employe_list, name='gestion_employe_list'),
    path('gestion_employe/new/', views.gerer_employe_new, name='gerer_employe_new'),
    path('gestion_employe/<int:employe_id>/', views.gerer_employe_detail, name='gerer_employe_detail'),
    path('gestion_employe/<int:gestion_id>/edit/', views.gerer_employe_edit, name='gerer_employe_edit'),
    path('gestion_employe/<int:gestion_id>/delete/', views.gerer_employe_delete, name='gerer_employe_delete'),
    
    path('pv/new/', views.pv_new, name='pv_new'),
]