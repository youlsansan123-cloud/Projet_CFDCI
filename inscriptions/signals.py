import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Etudiant, NotificationUtilisateur, Paiement


logger = logging.getLogger(__name__)


def _send_mail_safe(subject, message, recipient):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
    except Exception as exc:
        logger.warning("Echec envoi email a %s: %s", recipient, exc)


@receiver(pre_save, sender=Etudiant)
def memoriser_ancien_statut(sender, instance, **kwargs):
    if not instance.pk:
        instance._ancien_statut = None
        return

    try:
        ancien = Etudiant.objects.get(pk=instance.pk)
        instance._ancien_statut = ancien.statut
    except Etudiant.DoesNotExist:
        instance._ancien_statut = None


@receiver(post_save, sender=Etudiant)
def envoyer_notifications_etudiant(sender, instance, created, **kwargs):
    if created:
        NotificationUtilisateur.objects.create(
            etudiant=instance,
            titre='Inscription enregistree',
            message=(
                f"Bonjour {instance.prenom}, votre inscription a la formation "
                f"{instance.formation.nom} est enregistree et en attente de validation."
            ),
        )
        _send_mail_safe(
            subject='Inscription recue - en attente de validation',
            message=(
                f"Bonjour {instance.prenom},\n\n"
                f"Votre inscription a la formation {instance.formation.nom} est bien enregistree.\n"
                'Statut actuel: En attente de validation par un administrateur.\n\n'
                'Nous vous informerons des que votre inscription sera validee.'
            ),
            recipient=instance.email,
        )
        return

    ancien_statut = getattr(instance, '_ancien_statut', None)
    paiement = Paiement.objects.filter(etudiant=instance).first()

    if instance.statut == 'VALIDE':
        if paiement is None:
            Paiement.objects.create(
                etudiant=instance,
                montant=instance.formation.prix,
                statut='VALIDE',
            )
        else:
            champs_paiement_a_mettre_a_jour = []
            if paiement.montant != instance.formation.prix:
                paiement.montant = instance.formation.prix
                champs_paiement_a_mettre_a_jour.append('montant')
            if paiement.statut != 'VALIDE':
                paiement.statut = 'VALIDE'
                champs_paiement_a_mettre_a_jour.append('statut')
            if champs_paiement_a_mettre_a_jour:
                paiement.save(update_fields=champs_paiement_a_mettre_a_jour)
    elif paiement is not None:
        paiement.delete()

    if ancien_statut != 'VALIDE' and instance.statut == 'VALIDE':
        NotificationUtilisateur.objects.create(
            etudiant=instance,
            titre='Inscription validee',
            message=(
                f"Bonjour {instance.prenom}, votre inscription a la formation "
                f"{instance.formation.nom} a ete validee par l administrateur."
            ),
        )
        _send_mail_safe(
            subject='Inscription validee',
            message=(
                f"Bonjour {instance.prenom},\n\n"
                f"Votre inscription a la formation {instance.formation.nom} a ete validee.\n\n"
                'Merci.'
            ),
            recipient=instance.email,
        )
    elif ancien_statut != 'REFUSE' and instance.statut == 'REFUSE':
        NotificationUtilisateur.objects.create(
            etudiant=instance,
            titre='Inscription refusee',
            message=(
                f"Bonjour {instance.prenom}, votre inscription a la formation "
                f"{instance.formation.nom} a ete refusee."
            ),
        )
        _send_mail_safe(
            subject='Inscription refusee',
            message=(
                f"Bonjour {instance.prenom},\n\n"
                f"Votre inscription a la formation {instance.formation.nom} a ete refusee.\n\n"
                'Merci.'
            ),
            recipient=instance.email,
        )


@receiver(post_save, sender=Paiement)
def synchroniser_statut_etudiant_apres_validation_paiement(sender, instance, **kwargs):
    etudiant = instance.etudiant
    nouveau_statut = None

    if instance.statut == 'VALIDE':
        nouveau_statut = 'VALIDE'
    elif instance.statut == 'REFUSE':
        nouveau_statut = 'REFUSE'

    if nouveau_statut and etudiant.statut != nouveau_statut:
        etudiant.statut = nouveau_statut
        etudiant.save(update_fields=['statut'])
