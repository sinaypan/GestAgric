# GestAgric

Bienvenue dans GestAgric ! Un projet Django qui vous donne un accès à un système de gestion pour votre entreprise agricole.

## Prérequis

### A. Installation des dépendances

1. Téléchargez et installez une version récente de Python 3 depuis le site officiel : [Télécharger Python](https://www.python.org/downloads/) (N’oubliez pas de cocher l’option « Add Python to PATH » lors de l’installation).

2. Copiez ce répertoire dans votre dossier, par exemple TP1.

3. À partir de votre répertoire de projet, ouvrez l'interpréteur de ligne de commande (cmd).
   * Les commandes suivantes seront exécutées à l'aide de cet interpréteur de ligne de commande.

   - Créez un environnement virtuel pour isoler vos dépendances de packages localement:

     ```bash
     python -m venv env_name
     ```

   - Activez l'environnement virtuel précédemment créé:

     - Linux:

       ```bash
       source env_name/bin/activate
       ```

     - Windows:

       ```bash
       env_name\Scripts\activate
       ```

   - Installez le framework Django dans l'environnement virtuel:

     ```bash
     pip install django
     ```

   - Installez la bibliothèque de graphiques matplotlib dans l'environnement virtuel:

     ```bash
     pip install matplotlib
     ```
      La bibliothèque MATLAB comprend un large éventail de fonctions intégrées qui permettent aux utilisateurs de réaliser des tâches telles que le traitement du signal, la modélisation mathématique, la simulation, l'analyse de données, la visualisation, et bien plus encore. Ces fonctions couvrent divers domaines des mathématiques appliquées et des sciences de l'ingénieur.



4. Fermez le terminal.

### B. Lancement du projet

Une fois tout installé, voici comment lancer le projet à chaque fois :

1. À partir de votre répertoire de projet, ouvrez l'interpréteur de ligne de commande (cmd).
   * Les commandes suivantes seront exécutées à l'aide de cet interpréteur de ligne de commande.

   - Activez l'environnement virtuel précédemment créé:

     - Linux:

       ```bash
       source env_name/bin/activate
       ```

     - Windows:

       ```bash
       env_name\Scripts\activate
       ```

   - Accédez au dossier "gestagric" de votre répertoire de projet:

     ```bash
     cd gestagric
     ```

   - Lancez le serveur Django sur une machine locale:

     ```bash
     python manage.py runserver
     ```

   - Ouvrez un navigateur web et visitez le lien suivant:

     [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

    -le manager se connecte avec ses identifiants :

      identifiant : yanis 
      mot de passe : yanis

Ce projet est sous licence [ISILAAGENCYPROTECTION] - consultez le fichier LICENSE pour plus de détails.