from django.contrib import admin
from .models import MessageContact

@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'sujet', 'date_envoi')
    search_fields = ('nom', 'email', 'sujet', 'message')
