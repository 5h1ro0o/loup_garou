# Projet Loup-Garou - Groupe 7 (Florian & Matteo)

Le but est de concevoir et mettre en place le serveur TCP, qui assure la communication entre les clients et les moteurs du jeu.

**Description du projet**

Le projet "Loup-Garou" est une application distribuée composée de plusieurs modules qui interagissent ensemble :

- **Clients** : interfaces en TCP (terminal ou Tkinter) et en HTTP.
- **Serveurs** : un serveur TCP (réalisé par notre groupe) et un serveur HTTP (groupe 3).
- **Moteurs** : moteur d'administration et moteur de jeu.
- **Base de données** : SQLite3 pour stocker les informations importantes.

**Notre rôle - Groupe 7**

Nous sommes chargés de :

- Développer le serveur TCP.
- Gérer les connexions simultanées des clients TCP.
- Faire transiter les requêtes entre les clients et les moteurs (administration et jeu).
- Rendre le serveur robuste : gestion des erreurs, des déconnexions et des requêtes en parallèle.

**Technologies utilisées**

- Python 3.10+
- Sockets TCP/IP
- Multithreading (ou asyncio selon les besoins)
- gRPC pour la communication avec les moteurs

**Démarrer le serveur**

Pour lancer le serveur, exécutez simplement :

```bash
python server.py


Fonctionnement du serveur TCP
Le serveur démarre et écoute sur un port TCP.

Les clients (en terminal ou via interface graphique) se connectent.

Le serveur reçoit leurs requêtes.

Il les transmet au moteur concerné via gRPC.

Il renvoie ensuite la réponse du moteur au bon client.

L’objectif est de maintenir une communication fluide et fiable entre les clients et les moteurs.

Auteurs
Florian (Groupe 7)

Matteo (Groupe 7)

