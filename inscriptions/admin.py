from django.contrib import admin
from django.db.models import Case, IntegerField, Value, When
from django.template.response import TemplateResponse
from django.urls import path
from .models import (
    ComptePaiement,
    Etudiant,
    Formation,
    MembreEquipe,
    MessageContact,
    NotificationUtilisateur,
    Organisation,
    Paiement,
)


admin.site.site_header = "Gestion des Etudiants"
admin.site.site_title = "Administration"
admin.site.index_title = "Bienvenue sur le tableau de bord"


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = [
        'numero_etudiant',
        'nom',
        'prenom',
        'email',
        'formation',
        'statut',
        'est_actif',
        'created_at',
    ]
    list_filter = ['statut', 'formation', 'est_actif', 'created_at']
    search_fields = ['nom', 'prenom', 'email', 'numero_etudiant']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'date_naissance', 'email', 'telephone')
        }),
        ('Inscription', {
            'fields': ('formation', 'statut')
        }),
        ('Adresse', {
            'fields': ('ville', 'pays')
        }),
        ('Systeme', {
            'fields': ('numero_etudiant', 'est_actif', 'created_at', 'updated_at')
        }),
    )


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = (
        'nom',
        'prix',
        'duree',
        'capacite_max',
        'date_debut',
        'date_fin',
        'est_active',
    )
    list_filter = ('est_active', 'date_debut')
    search_fields = ('nom',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ComptePaiement)
class ComptePaiementAdmin(admin.ModelAdmin):
    list_display = ('operateur', 'numero_telephone', 'titulaire', 'est_actif', 'updated_at')
    list_filter = ('operateur', 'est_actif')
    search_fields = ('numero_telephone', 'titulaire')
    change_list_template = 'admin/inscriptions/comptepaiement/change_list.html'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
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

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'moyens-paiement/',
                self.admin_site.admin_view(self.moyens_paiement_view),
                name='inscriptions_comptepaiement_moyens_paiement',
            ),
        ]
        return custom_urls + urls

    def moyens_paiement_view(self, request):
        comptes = self.get_queryset(request)
        context = {
            **self.admin_site.each_context(request),
            'title': 'Moyens de paiement',
            'comptes': comptes,
            'opts': self.model._meta,
        }
        return TemplateResponse(request, 'admin/inscriptions/moyens_paiement.html', context)


@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'montant', 'statut', 'date_paiement')
    list_filter = ('statut', 'date_paiement')
    search_fields = ('etudiant__nom', 'etudiant__prenom', 'etudiant__email')
    readonly_fields = ('date_paiement',)


@admin.register(NotificationUtilisateur)
class NotificationUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'titre', 'est_lue', 'created_at')
    list_filter = ('est_lue', 'created_at')
    search_fields = ('etudiant__nom', 'etudiant__prenom', 'etudiant__email', 'titre', 'message')
    readonly_fields = ('created_at',)


class MembreEquipeInline(admin.TabularInline):
    model = MembreEquipe
    extra = 1
    fields = ('nom', 'role', 'ordre_affichage')


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email_officiel', 'telephone_officiel', 'updated_at')
    search_fields = ('nom', 'email_officiel', 'telephone_officiel')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [MembreEquipeInline]


@admin.register(MembreEquipe)
class MembreEquipeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'role', 'organisation', 'ordre_affichage')
    list_filter = ('organisation',)
    search_fields = ('nom', 'role', 'organisation__nom')


@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'est_traite', 'created_at')
    list_filter = ('est_traite', 'created_at')
    search_fields = ('nom', 'email', 'message')
    readonly_fields = ('created_at',)
