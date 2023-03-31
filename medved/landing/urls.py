from django.urls import path
from .views import landing, home

urlpatterns = [
    path('', home, name='home'),
    path('landing/', landing, name='landing')
]