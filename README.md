# 📚 Application Web d'Inscription à une Formation

[![Django](https://img.shields.io/badge/Django-6.0.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📖 Description du Projet

Cette application web Django permet de simuler et gérer le processus complet d'inscription en ligne pour des formations professionnelles. Développée dans le cadre d'un projet académique, elle offre une interface utilisateur intuitive pour les étudiants et un panneau d'administration complet pour les gestionnaires.

### 🎯 Fonctionnalités Principales

- **👨‍🎓 Gestion des Étudiants** : Inscription, suivi des statuts, informations personnelles
- **📚 Gestion des Formations** : Création et administration des programmes de formation
- **💳 Système de Paiement** : Intégration de multiples moyens de paiement (Orange Money, MTN Money, Wave, etc.)
- **📊 Interface d'Administration** : Panneau complet pour gérer toutes les données
- **📧 Notifications** : Système de notifications pour les utilisateurs
- **🎨 Interface Personnalisable** : Thèmes admin personnalisables via django-admin-interface
- **🏢 Gestion d'Organisation** : Structure organisationnelle avec membres d'équipe

### 🏗️ Architecture Technique

#### Modèles Principaux
- **Formation** : Informations sur les programmes (nom, prix, durée, capacité)
- **Étudiant** : Données personnelles et statut d'inscription
- **Paiement** : Gestion des transactions et statuts
- **ComptePaiement** : Configuration des opérateurs de paiement
- **NotificationUtilisateur** : Système de messagerie interne
- **Organisation** : Structure organisationnelle
- **MembreEquipe** : Équipe et rôles

#### Technologies Utilisées
- **Backend** : Django 6.0.2, Python 3.11+
- **Base de Données** : SQLite (développement) / PostgreSQL (production)
- **Frontend** : HTML5, CSS3, Bootstrap (via templates Django)
- **Authentification** : Django Auth intégré
- **Interface Admin** : Django Admin + django-admin-interface + django-colorfield

## 🚀 Installation et Déploiement

### Prérequis
- Python 3.11+
- pip (gestionnaire de paquets Python)

### Installation Locale

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/votre-utilisateur/inscription-formation.git
   cd inscription-formation
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   # Sur Windows
   venv\Scripts\activate
   # Sur Linux/Mac
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   pip install django-admin-interface django-colorfield
   ```

4. **Configurer la base de données**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Créer un superutilisateur (admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Lancer le serveur**
   ```bash
   python manage.py runserver
   ```

7. **Accéder à l'application**
   - Site étudiant : http://127.0.0.1:8000
   - Interface admin : http://127.0.0.1:8000/admin

### Déploiement sur Replit

1. Importer depuis GitHub dans une nouvelle Repl Python
2. Configurer les secrets dans Replit :
   - `DJANGO_SECRET_KEY` : Votre clé secrète
   - `DJANGO_DEBUG` : `False`
   - `DJANGO_ALLOWED_HOSTS` : `*`
3. Modifier le run command :
   ```bash
   python manage.py migrate && python manage.py runserver 0.0.0.0:8000
   ```

## 📁 Structure du Projet

```
inscription_formation/
├── inscription_formation/          # Configuration Django
│   ├── settings.py                # Paramètres principaux
│   ├── urls.py                    # Routes principales
│   └── wsgi.py                    # Configuration WSGI
├── inscriptions/                   # Application principale
│   ├── models.py                  # Modèles de données
│   ├── views.py                   # Logique métier
│   ├── admin.py                   # Configuration admin
│   ├── templates/                 # Templates HTML
│   ├── static/                    # CSS, JS, images
│   └── migrations/                # Migrations DB
├── media/                         # Fichiers uploadés
├── staticfiles/                   # Fichiers statiques collectés
├── manage.py                      # Script de gestion Django
├── requirements.txt               # Dépendances Python
└── README.md                      # Documentation
```

## 🔧 Configuration

### Variables d'Environnement
```bash
# Sécurité
DJANGO_SECRET_KEY=votre-cle-secrete-unique
DJANGO_DEBUG=False

# Base de données (optionnel pour PostgreSQL)
DB_NAME=votre_db
DB_USER=votre_user
DB_PASSWORD=votre_password
DB_HOST=localhost
DB_PORT=5432

# Email (optionnel)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe
```

### Paramètres Django
- **Langue** : Français (fr)
- **Fuseau horaire** : Afrique/Abidjan
- **Authentification** : Django Auth intégré
- **Sessions** : Base de données

## 📊 Modélisation UML

Le projet inclut une analyse complète avec :

- **Diagrammes de cas d'utilisation** : Identification des acteurs et fonctionnalités
- **Diagrammes de séquence** : Flux d'inscription et paiement
- **Diagrammes de classes** : Structure des modèles et relations

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📝 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👤 Auteur

**Youl Sansan Fulgence**
- Email : youlsansan123@gmail.com
- Date : Mars 2026

---

⭐ Si ce projet vous plaît, n'hésitez pas à lui donner une étoile !



