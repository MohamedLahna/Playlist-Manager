# 🎵 Playlist Manager

Une application de bureau basée sur **Python** et **Tkinter** permettant de gérer, réorganiser et lire des playlists audio. L'application s'appuie sur une base de données **MySQL** pour la persistance des données et intègre la prise en charge de l'asynchronisme avec `asyncio`.

## ✨ Fonctionnalités

* **Gestion de Playlists :** Ajout et suppression de morceaux.
* **Réorganisation intuitive :** Réordonnancement et tri des titres par glisser-déposer (Drag & Drop).
* **Persistance des données :** Sauvegarde et chargement automatique depuis une base de données MySQL.
* **Lecture Audio :** Intégration du module `pygame` pour la lecture des fichiers audio.
* **Architecture Asynchrone :** Boucle d'événements fluide combinant `asyncio` et Tkinter.
* **Compatibilité Web / Emscripten :** Détection de l'environnement pour une exécution possible via Pyodide.

## 🛠️ Technologies Utilisées

* **Langage :** Python 3.x
* **Interface Graphique :** Tkinter
* **Base de Données :** MySQL (`mysql-connector-python`)
* **Moteur Audio :** Pygame
* **Programmation Asynchrone :** Asyncio

## 🗄️ Structure de la Base de Données

Le schéma de la base de données est structuré comme suit (fichier `Morceau.sql`) :

```sql
CREATE DATABASE IF NOT EXISTS playlist_db;
USE playlist_db;

-- Table pour stocker les pistes audio
CREATE TABLE IF NOT EXISTS morceaux (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(255) NOT NULL,
    artiste VARCHAR(255) NOT NULL,
    chemin_fichier VARCHAR(255) NOT NULL
);

-- Table pour la gestion de l'ordre des playlists
CREATE TABLE IF NOT EXISTS playlists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    morceau_id INT NULL,
    ordre INT NULL,
    FOREIGN KEY (morceau_id) REFERENCES morceaux(id) ON DELETE CASCADE
);
