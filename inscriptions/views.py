from django.contrib import messages
from django.core.mail import send_mail
from django.db import OperationalError, ProgrammingError
from django.db.models import Case, IntegerField, Value, When
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import EtudiantForm, MessageContactForm
from .models import ComptePaiement, Etudiant, Formation, MembreEquipe, Organisation


def _comptes_paiement_ordonnes_queryset():
    return ComptePaiement.objects.annotate(
        priorite=Case(
            When(operateur='ORANGE_MONEY', then=Value(1)),
            When(operateur='MTN_MONEY', then=Value(2)),
            When(operateur='MOOV_MONEY', then=Value(3)),
            When(operateur='WAVE', then=Value(4)),
            When(operateur='TRESOR_MONEY', then=Value(5)),
            When(operateur='DJAMO', then=Value(6)),
            default=Value(99),
            output_field=IntegerField(),
        )
    ).order_by('priorite', 'numero_telephone')


def _inscription_context(form):
    formations = Formation.objects.filter(est_active=True).order_by('nom')
    comptes_paiement = _comptes_paiement_ordonnes_queryset().filter(est_actif=True)
    return {
        'form': form,
        'formations_data': [formation.as_dict() for formation in formations],
        'comptes_paiement': comptes_paiement,
    }


def _get_organisation():
    try:
        return Organisation.objects.prefetch_related('membres_equipe').first()
    except (OperationalError, ProgrammingError):
        return None


def accueil(request):
    organisation = _get_organisation()
    return render(request, 'inscriptions/site/accueil.html', {'organisation': organisation})


def a_propos(request):
    organisation = _get_organisation()
    if organisation:
        membres = MembreEquipe.objects.filter(organisation=organisation) | MembreEquipe.objects.filter(organisation__isnull=True)
    else:
        membres = MembreEquipe.objects.all()
    membres = membres.order_by('ordre_affichage', 'nom')
    return render(
        request,
        'inscriptions/site/a_propos.html',
        {
            'organisation': organisation,
            'membres': membres,
        },
    )


def contact(request):
    organisation = _get_organisation()
    form = MessageContactForm()
    success_sent = request.GET.get('sent') == '1'
    if request.method == 'POST':
        form = MessageContactForm(request.POST)
        if form.is_valid():
            try:
                message_contact = form.save()
            except (OperationalError, ProgrammingError):
                messages.error(
                    request,
                    "Le module contact n est pas encore initialise. Lancez d abord les migrations.",
                )
                return redirect('contact')
            destinataire = organisation.email_officiel if organisation and organisation.email_officiel else None
            if destinataire:
                send_mail(
                    subject=f"Nouveau message de contact - {message_contact.nom}",
                    message=message_contact.message,
                    from_email=message_contact.email,
                    recipient_list=[destinataire],
                    fail_silently=True,
                )
            return redirect(f"{reverse('contact')}?sent=1")

    return render(
        request,
        'inscriptions/site/contact.html',
        {
            'organisation': organisation,
            'form': form,
            'success_sent': success_sent,
        },
    )


def inscription_etudiant(request):
    form = EtudiantForm()
    if request.method == 'POST':
        form = EtudiantForm(request.POST)
        if form.is_valid():
            etudiant = form.save(commit=False)
            etudiant.statut = 'EN_ATTENTE'
            etudiant.save()
            messages.success(
                request,
                'Inscription enregistree. Apres verification du paiement par l administrateur, votre statut et votre notification seront mis a jour automatiquement.',
            )
            return redirect('inscription')
    return render(request, 'inscriptions/inscription.html', _inscription_context(form))


def ajouter_etudiant(request):
    form = EtudiantForm()
    if request.method == 'POST':
        form = EtudiantForm(request.POST)
        if form.is_valid():
            etudiant = form.save(commit=False)
            etudiant.statut = 'EN_ATTENTE'
            etudiant.save()
            messages.success(
                request,
                'Etudiant ajoute avec statut En attente. L administrateur validera apres verification du paiement.',
            )
            return redirect('inscription')
    return render(request, 'inscriptions/ajouter_etudiant.html', _inscription_context(form))


def suivi_inscription(request):
    email = (request.GET.get('email') or '').strip()
    etudiant = None
    paiement = None
    notifications = []
    if email:
        etudiant = Etudiant.objects.filter(email__iexact=email).select_related('formation', 'paiement').first()
        if etudiant is None:
            messages.warning(request, "Aucune inscription trouvee pour cet email.")
        else:
            try:
                paiement = etudiant.paiement
            except Etudiant.paiement.RelatedObjectDoesNotExist:
                paiement = None
            notifications = list(etudiant.notifications.all()[:10])

    return render(
        request,
        'inscriptions/suivi_inscription.html',
        {
            'email': email,
            'etudiant': etudiant,
            'paiement': paiement,
            'notifications': notifications,
        },
    )
