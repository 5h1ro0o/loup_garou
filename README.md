# Projet Loup-Garou - Groupe 7 (Florian & Matteo)

Bienvenue dans notre dépôt Git pour le projet **Loup-Garou** réalisé dans le cadre de notre 3ᵉ année d'informatique.

Notre mission au sein de ce projet consiste à développer le **Serveur TCP**, qui permet la communication entre les clients TCP et les moteurs du jeu.

---

## 📚 Description du projet global

Le projet "Loup-Garou" est une application distribuée basée sur plusieurs modules interconnectés :  
- **Clients** : Interfaces utilisateur via TCP ou HTTP (terminal ou Tkinter).
- **Serveurs** : Serveur TCP (groupe 7) et Serveur HTTP (groupe 3).
- **Moteurs** : Moteur d'administration et moteur de jeu.
- **Base de données** : SQLite3 pour stocker les informations essentielles.

---

## 🎯 Notre rôle - Groupe 7

Nous (Florian et Matteo) sommes responsables de :
- Développer un **Serveur TCP**.
- Gérer les connexions multiples des clients TCP (interface Terminal ou Tkinter).
- Faire transiter les requêtes entre les clients TCP et les moteurs (administration/jeu) via des communications réseau.
- Assurer la robustesse du serveur : gestion des erreurs, des déconnexions, des requêtes simultanées.

---

## 🔧 Technologies utilisées

- **Python 3.10+**
- **Sockets TCP/IP**
- **Multithreading** (ou asyncio selon l'optimisation)
- **gRPC** pour la communication avec les moteurs
- 
---

## 🖥️ Fonctionnement de notre Serveur TCP

1. Le serveur démarre et écoute sur un port TCP défini.
2. Les clients TCP (terminal ou interface graphique) se connectent au serveur.
3. Le serveur reçoit les requêtes des clients.
4. Il relaie les requêtes vers le moteur d'administration ou de jeu via gRPC.
5. Il renvoie les réponses des moteurs aux clients correspondants.

**Objectif principal** : garantir une communication fluide et fiable entre les clients et les moteurs.

---

## ⚙️ Lancer le serveur

```bash
python server.py
```
Veillez à ce que les moteurs soient disponibles avant de lancer le serveur.

📜 Schéma d'architecture générale

✨ Auteurs
Florian (Groupe 7)

Matteo (Groupe 7)
