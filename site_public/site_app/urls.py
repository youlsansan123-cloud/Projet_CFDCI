from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('a-propos/', views.a_propos, name='a_propos'),
    path('contact/', views.contact, name='contact'),
    path('inscription/', views.inscription_etudiant, name='inscription'),
    path('inscription/suivi/', views.suivi_inscription, name='suivi_inscription'),
]