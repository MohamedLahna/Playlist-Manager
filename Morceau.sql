CREATE DATABASE IF NOT EXISTS playlist_db;

USE playlist_db;

-- Table pour les morceaux
CREATE TABLE IF NOT EXISTS morceaux (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(255) NOT NULL,
    artiste VARCHAR(255) NOT NULL,
    chemin_fichier VARCHAR(255) NOT NULL
);

-- Table pour les playlists
CREATE TABLE IF NOT EXISTS playlists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    morceau_id INT NULL,
    ordre INT NULL,
    FOREIGN KEY (morceau_id) REFERENCES morceaux(id) ON DELETE CASCADE
);
