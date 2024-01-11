from django.contrib import admin
from django.urls import path, include
from utilisateur.views import home  # Import the home view from the entrepot app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # This line sets the root URL to the home view of the entrepot app
    path('Entrepot/', include('entrepot.urls')),
    path('gestionCentre/', include('gestionCentre.urls')),
    path('utilisateur/', include('utilisateur.urls')),
]
