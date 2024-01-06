from django.urls import path
from . import views

#app_name = 'entrepot'

urlpatterns = [

    path('home/', views.home, name='home'),

    path('fournisseurs/', views.fournisseur_list, name='fournisseur_list'),
    path('fournisseur/new/', views.fournisseur_new, name='fournisseur_new'),
    path('fournisseur/<int:pk>/', views.fournisseur_detail, name='fournisseur_detail'),
    path('fournisseur/<int:pk>/edit/', views.fournisseur_edit, name='fournisseur_edit'),
    path('fournisseur/<int:pk>/delete/', views.fournisseur_delete, name='fournisseur_delete'),

    path('produits/', views.produit_list, name='produit_list'),
    path('produit/new/', views.produit_new, name='produit_new'),
    path('produit/<int:pk>/', views.produit_detail, name='produit_detail'),
    path('produit/<int:pk>/edit/', views.produit_edit, name='produit_edit'),
    path('produit/<int:pk>/delete/', views.produit_delete, name='produit_delete'),

    path('achats/', views.Achat_list, name='achat_list'),
    path('achat/new/', views.Achat_new, name='achat_new'),
    path('achat/<int:pk>/', views.Achat_detail, name='achat_detail'),
    path('achat/<int:pk>/edit/', views.Achat_edit, name='achat_edit'),
    path('achat/<int:pk>/delete/', views.Achat_delete, name='achat_delete'),
    path('fournisseur/new1/', views.fournisseur_new1, name='fournisseur_new1'),
    path('produit/new1/', views.produit_new1, name='produit_new1'),

    path('transferts/', views.Transfert_list, name='transfert_list'),
    path('transfert/new/', views.Transfert_new, name='transfert_new'),
    path('transfert/<int:pk>/', views.Transfert_detail, name='transfert_detail'),
    path('transfert/<int:pk>/edit/', views.Transfert_edit, name='transfert_edit'),
    path('transfert/<int:pk>/delete/', views.Transfert_delete, name='transfert_delete'),

    path('ventes/', views.Vente_list, name='vente_list'),
    path('vente/new/', views.Vente_new, name='vente_new'),
    path('vente/<int:pk>/', views.Vente_detail, name='vente_detail'),
    path('vente/<int:pk>/edit/', views.Vente_edit, name='vente_edit'),
    path('vente/<int:pk>/delete/', views.Vente_delete, name='vente_delete'),
    path('vente/completer/<int:pk>/', views.vente_completer, name='vente_completer'),
    

    path('etat-stock/', views.etat_stock, name='etat_stock'),
]
