from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


def accueil(request):
    """Page d'accueil du site"""
    context = {
        'titre': 'Bienvenue sur notre plateforme de formation',
        'description': 'Découvrez nos programmes de formation professionnelle',
    }
    return render(request, 'site_app/accueil.html', context)


def a_propos(request):
    """Page à propos"""
    context = {
        'titre': 'À propos de nous',
        'description': 'Notre mission est de former les professionnels de demain',
    }
    return render(request, 'site_app/a_propos.html', context)


def contact(request):
    """Page de contact"""
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')

        # Ici vous pouvez ajouter la logique d'envoi d'email
        # send_mail(sujet, message, email, [settings.DEFAULT_FROM_EMAIL])

        messages.success(request, 'Votre message a été envoyé avec succès !')
        return render(request, 'site_app/contact.html')

    context = {
        'titre': 'Contactez-nous',
        'description': 'Nous sommes là pour répondre à vos questions',
    }
    return render(request, 'site_app/contact.html', context)


def inscription_etudiant(request):
    """Page d'inscription étudiant (simplifiée pour démo)"""
    context = {
        'titre': 'Inscription à une formation',
        'description': 'Rejoignez-nous pour développer vos compétences',
        'formations_disponibles': [
            {'nom': 'Développement Web', 'prix': 150000, 'duree': 3},
            {'nom': 'Data Science', 'prix': 200000, 'duree': 4},
            {'nom': 'Intelligence Artificielle', 'prix': 250000, 'duree': 5},
        ]
    }
    return render(request, 'site_app/inscription.html', context)


def suivi_inscription(request):
    """Page de suivi d'inscription (simplifiée)"""
    numero_etudiant = request.GET.get('numero')

    context = {
        'titre': 'Suivi de votre inscription',
        'numero_recherche': numero_etudiant,
        'message': 'Fonctionnalité de suivi en développement'
    }
    return render(request, 'site_app/suivi_inscription.html', context)
