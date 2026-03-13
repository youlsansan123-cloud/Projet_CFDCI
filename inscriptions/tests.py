from datetime import date, timedelta

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import ComptePaiement, Etudiant, Formation, NotificationUtilisateur, Paiement


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class InscriptionWorkflowTests(TestCase):
    def setUp(self):
        self.formation = Formation.objects.create(
            nom='Python Web',
            description='Formation Django',
            prix=100000,
            duree=40,
            capacite_max=30,
            date_debut=date.today() + timedelta(days=7),
            date_fin=date.today() + timedelta(days=30),
            est_active=True,
        )

    def test_nouvel_etudiant_est_en_attente_et_recoit_mail(self):
        etudiant = Etudiant.objects.create(
            nom='Doe',
            prenom='Jane',
            email='jane@example.com',
            telephone='0102030405',
            formation=self.formation,
            ville='Abidjan',
            pays='Cote d Ivoire',
            date_naissance=date(2000, 1, 1),
        )

        self.assertEqual(etudiant.statut, 'EN_ATTENTE')
        self.assertFalse(Paiement.objects.filter(etudiant=etudiant).exists())
        self.assertEqual(NotificationUtilisateur.objects.filter(etudiant=etudiant).count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('en attente', mail.outbox[0].subject.lower())

    def test_mail_envoye_quand_statut_devient_valide(self):
        etudiant = Etudiant.objects.create(
            nom='Doe',
            prenom='John',
            email='john@example.com',
            telephone='0504030201',
            formation=self.formation,
            ville='Abidjan',
            pays='Cote d Ivoire',
            date_naissance=date(1999, 5, 5),
        )

        self.assertEqual(len(mail.outbox), 1)

        etudiant.statut = 'VALIDE'
        etudiant.save()
        etudiant.refresh_from_db()

        self.assertEqual(len(mail.outbox), 2)
        self.assertIn('validee', mail.outbox[1].subject.lower())
        self.assertEqual(NotificationUtilisateur.objects.filter(etudiant=etudiant).count(), 2)
        self.assertEqual(etudiant.paiement.statut, 'VALIDE')

    def test_validation_paiement_met_a_jour_statut_etudiant(self):
        etudiant = Etudiant.objects.create(
            nom='Doe',
            prenom='Sara',
            email='sara@example.com',
            telephone='0101010101',
            formation=self.formation,
            ville='Abidjan',
            pays='Cote d Ivoire',
            date_naissance=date(2001, 3, 3),
        )
        paiement = Paiement.objects.create(
            etudiant=etudiant,
            montant=100000,
            statut='EN_ATTENTE',
        )

        paiement.statut = 'VALIDE'
        paiement.save(update_fields=['statut'])
        etudiant.refresh_from_db()

        self.assertEqual(etudiant.statut, 'VALIDE')
        self.assertEqual(NotificationUtilisateur.objects.filter(etudiant=etudiant).count(), 2)

    def test_validation_etudiant_met_a_jour_statut_paiement(self):
        etudiant = Etudiant.objects.create(
            nom='Doe',
            prenom='Moussa',
            email='moussa@example.com',
            telephone='0101010102',
            formation=self.formation,
            ville='Abidjan',
            pays='Cote d Ivoire',
            date_naissance=date(2001, 1, 1),
        )

        etudiant.statut = 'VALIDE'
        etudiant.save(update_fields=['statut'])
        etudiant.refresh_from_db()

        self.assertEqual(etudiant.paiement.statut, 'VALIDE')

    def test_notification_visible_dans_suivi_apres_validation(self):
        etudiant = Etudiant.objects.create(
            nom='Doe',
            prenom='Mina',
            email='mina@example.com',
            telephone='0777777777',
            formation=self.formation,
            ville='Abidjan',
            pays='Cote d Ivoire',
            date_naissance=date(2000, 7, 7),
        )
        etudiant.statut = 'VALIDE'
        etudiant.save()

        response = self.client.get(reverse('suivi_inscription'), {'email': 'mina@example.com'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Notifications')
        self.assertContains(response, 'Inscription validee')

    def test_page_inscription_affiche_details_formation_et_comptes_paiement(self):
        ComptePaiement.objects.create(
            operateur='ORANGE_MONEY',
            numero_telephone='0700000000',
            titulaire='Centre Formation',
            est_actif=True,
        )

        response = self.client.get(reverse('inscription'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Web')
        self.assertContains(response, '0700000000')

    def test_ordre_prioritaire_comptes_paiement_sur_page_inscription(self):
        ComptePaiement.objects.create(operateur='DJAMO', numero_telephone='0600000000', est_actif=True)
        ComptePaiement.objects.create(operateur='ORANGE_MONEY', numero_telephone='0700000000', est_actif=True)
        ComptePaiement.objects.create(operateur='MTN_MONEY', numero_telephone='0500000000', est_actif=True)

        response = self.client.get(reverse('inscription'))

        comptes = list(response.context['comptes_paiement'])
        self.assertEqual(comptes[0].operateur, 'ORANGE_MONEY')
        self.assertEqual(comptes[1].operateur, 'MTN_MONEY')
        self.assertEqual(comptes[2].operateur, 'DJAMO')

    def test_suivi_inscription_affiche_statut(self):
        Etudiant.objects.create(
            nom='Doe',
            prenom='Alice',
            email='alice@example.com',
            telephone='0701010101',
            formation=self.formation,
            ville='Abidjan',
            pays='Cote d Ivoire',
            date_naissance=date(2001, 2, 2),
        )

        response = self.client.get(reverse('suivi_inscription'), {'email': 'alice@example.com'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice Doe')
        self.assertContains(response, 'En attente')
