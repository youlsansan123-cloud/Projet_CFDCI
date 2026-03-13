from django.urls import path
from . import views

urlpatterns = [
    path('organisation/', views.accueil, name='accueil'),
    path('organisation/a-propos/', views.a_propos, name='a_propos'),
    path('organisation/contact/', views.contact, name='contact'),
    path('inscription/', views.inscription_etudiant, name='inscription'),
    path('inscription/suivi/', views.suivi_inscription, name='suivi_inscription'),
    # Legacy aliases to keep older links working.
    path('inscriptions/ajouter/', views.inscription_etudiant, name='inscriptions_ajouter_legacy'),
    path('inscriptions/suivi/', views.suivi_inscription, name='inscriptions_suivi_legacy'),
]
