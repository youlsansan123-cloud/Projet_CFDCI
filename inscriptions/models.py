from django.db import models
from django.utils import timezone


# ============================
#       FORMATION
# ============================

class Formation(models.Model):

    nom = models.CharField(max_length=200, verbose_name="Nom de la formation")
    description = models.TextField(verbose_name="Description")
    prix = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    duree = models.PositiveIntegerField(help_text="Durée en heures", verbose_name="Durée")
    capacite_max = models.PositiveIntegerField(verbose_name="Capacité maximale")

    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(verbose_name="Date de fin")

    est_active = models.BooleanField(default=True, verbose_name="Active")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"
        ordering = ['-date_debut']

    def __str__(self):
        return f"{self.nom} - {self.prix} FCFA"

    # Nombre d'étudiants inscrits
    def nombre_inscrits(self):
        return self.etudiants.count()

    # Vérifie si la formation est complète
    def est_complete(self):
        return self.nombre_inscrits() >= self.capacite_max

    # Vérifie si la formation est disponible
    def est_disponible(self):
        return (
            self.est_active
            and not self.est_complete()
            and self.date_debut >= timezone.now().date()
        )

    def as_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'description': self.description,
            'prix': str(self.prix),
            'duree': self.duree,
            'capacite_max': self.capacite_max,
            'date_debut': self.date_debut.strftime('%d/%m/%Y'),
            'date_fin': self.date_fin.strftime('%d/%m/%Y'),
            'est_active': self.est_active,
        }


# ============================
#       ETUDIANT
# ============================

class Etudiant(models.Model):

    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('VALIDE', 'Validé'),
        ('REFUSE', 'Refusé'),
    ]

    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    email = models.EmailField(unique=True, verbose_name="Email")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")

    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='etudiants',
        verbose_name="Formation choisie"
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='EN_ATTENTE',
        verbose_name="Statut d'inscription"
    )

    ville = models.CharField(max_length=100, verbose_name="Ville")
    pays = models.CharField(max_length=100, default="Côte d'Ivoire", verbose_name="Pays")

    date_naissance = models.DateField(verbose_name="Date de naissance")

    numero_etudiant = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Numéro étudiant"
    )

    est_actif = models.BooleanField(default=True, verbose_name="Actif")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Étudiant"
        verbose_name_plural = "Étudiants"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def get_full_name(self):
        return f"{self.prenom} {self.nom}"


# ============================
#       PAIEMENT
# ============================

class Paiement(models.Model):

    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('VALIDE', 'Validé'),
        ('REFUSE', 'Refusé'),
    ]

    etudiant = models.OneToOneField(
        Etudiant,
        on_delete=models.CASCADE,
        related_name="paiement",
        verbose_name="Étudiant"
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant payé")

    date_paiement = models.DateTimeField(auto_now_add=True, verbose_name="Date du paiement")

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='EN_ATTENTE',
        verbose_name="Statut du paiement"
    )

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"

    def __str__(self):
        return f"{self.etudiant.get_full_name()} - {self.statut}"


# ============================
#   COMPTE DE PAIEMENT
# ============================

class ComptePaiement(models.Model):
    OPERATEUR_CHOICES = [
        ('ORANGE_MONEY', 'Orange Money'),
        ('MOOV_MONEY', 'Moov Money'),
        ('MTN_MONEY', 'MTN Money'),
        ('WAVE', 'Wave'),
        ('TRESOR_MONEY', 'Tresor Money'),
        ('DJAMO', 'Djamo'),
    ]

    operateur = models.CharField(
        max_length=20,
        choices=OPERATEUR_CHOICES,
        verbose_name='Operateur'
    )
    numero_telephone = models.CharField(max_length=20, verbose_name='Numero de telephone')
    titulaire = models.CharField(max_length=100, blank=True, verbose_name='Titulaire du compte')
    est_actif = models.BooleanField(default=True, verbose_name='Actif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Compte de paiement'
        verbose_name_plural = 'Comptes de paiement'
        ordering = ['operateur', 'numero_telephone']

    def __str__(self):
        return f"{self.get_operateur_display()} - {self.numero_telephone}"


class NotificationUtilisateur(models.Model):
    etudiant = models.ForeignKey(
        Etudiant,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Etudiant'
    )
    titre = models.CharField(max_length=150, verbose_name='Titre')
    message = models.TextField(verbose_name='Message')
    est_lue = models.BooleanField(default=False, verbose_name='Lue')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notification utilisateur'
        verbose_name_plural = 'Notifications utilisateur'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.etudiant.get_full_name()} - {self.titre}"


class Organisation(models.Model):
    nom = models.CharField(max_length=200, verbose_name='Nom de l organisation')
    presentation_generale = models.TextField(verbose_name='Presentation generale')
    mission = models.TextField(verbose_name='Mission')
    vision = models.TextField(verbose_name='Vision')
    histoire = models.TextField(verbose_name='Histoire')
    objectifs = models.TextField(verbose_name='Objectifs principaux')
    email_officiel = models.EmailField(blank=True, verbose_name='Email officiel')
    telephone_officiel = models.CharField(max_length=30, blank=True, verbose_name='Telephone officiel')
    adresse = models.CharField(max_length=255, blank=True, verbose_name='Adresse')
    image_banniere_url = models.URLField(blank=True, verbose_name='Image banniere (URL)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Organisation'
        verbose_name_plural = 'Organisation'

    def __str__(self):
        return self.nom


class MembreEquipe(models.Model):
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name='membres_equipe',
        verbose_name='Organisation',
        null=True,
        blank=True,
    )
    nom = models.CharField(max_length=120, verbose_name='Nom')
    role = models.CharField(max_length=120, verbose_name='Role')
    ordre_affichage = models.PositiveIntegerField(default=0, verbose_name='Ordre d affichage')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Membre equipe'
        verbose_name_plural = 'Membres equipe'
        ordering = ['ordre_affichage', 'nom']

    def __str__(self):
        return f"{self.nom} - {self.role}"


class MessageContact(models.Model):
    nom = models.CharField(max_length=120, verbose_name='Nom')
    email = models.EmailField(verbose_name='Email')
    message = models.TextField(verbose_name='Message')
    created_at = models.DateTimeField(auto_now_add=True)
    est_traite = models.BooleanField(default=False, verbose_name='Traite')

    class Meta:
        verbose_name = 'Message contact'
        verbose_name_plural = 'Messages contact'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nom} - {self.email}"
