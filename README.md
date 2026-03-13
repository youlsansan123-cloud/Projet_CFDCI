##### **Projet 4 : Simulation d’un Processus d’Inscription en Ligne pour une Formation.**





**Projet** : Application Web d’Inscription à une Formation

**Auteur** : Youl Sansan Fulgence

**Date** : Février 2026

**Technologies** : Python, Django



Description :

Ce projet est une application web permettant de simuler le processus

d'inscription en ligne pour une formation.



Qu'est-ce que Django ?

Django est un framework web Python qui permet de créer des applications web rapidement et efficacement. Il suit le principe Don't Repeat Yourself (DRY) et inclut tout ce dont on a  besoin pour développer.



**1. La partie théorique** : modélisation UML 



diagrammes de cas d’utilisation:

Le diagramme de cas d’utilisation permet d’identifier les acteurs du système et les fonctionnalités principales auxquelles ils ont accès.



diagrammes de séquence

Le diagramme de séquence décrit le déroulement temporel des interactions entre les acteurs et les objets du système pour un scénario donné, notamment le processus d’inscription et de paiement.





&nbsp;diagrammes et de classes.

Le diagramme de classes décrit la structure statique du système à travers les différentes classes, leurs attributs, leurs méthodes et leurs relations.







**2. La partie pratique** : application web Django avec interface pour les étudiants

&nbsp;  et administration.



---



Instructions pour exécuter le projet :



1\. Créer un environnement virtuel :

&nbsp;  python -m venv venv



2\. Activer l'environnement virtuel :



&nbsp;  # Sur Windows

&nbsp;  venv\\Scripts\\activate



&nbsp;  # Sur Linux / Mac

&nbsp;  source venv/bin/activate



3\. Installer les dépendances :

&nbsp;  pip install -r requirements.txt

&nbsp;  pip install django-widget-tweaks   # nécessaire pour certains formulaires



4\. Lancer le serveur Django :

&nbsp;  python manage.py runserver



5\. Accéder à l'application :

&nbsp;  - Formulaire d'inscription étudiant :

&nbsp;    http://127.0.0.1:8000/inscriptions/ajouter/

&nbsp;  - Interface d’administration Django :

&nbsp;    http://127.0.0.1:8000/admin

&nbsp;    (utiliser les identifiants créés lors de la configuration)



Remarques :

\- La base de données SQLite (db.sqlite3) contient les données créées.  

&nbsp; Si elle est supprimée, créer la base vide avec :



&nbsp;   python manage.py makemigrations

&nbsp;   python manage.py migrate



\- Les templates HTML pour les étudiants sont dans :

&nbsp; inscriptions/templates/inscriptions/etudiant\_form.html



\- Pour ajouter, modifier ou valider les inscriptions, utiliser l’interface admin Django.



\- Ce projet a été développé avec Django et est livré prêt à être exécuté

&nbsp; sur tout PC avec Python installé.



