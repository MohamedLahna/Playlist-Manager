import pygame
import asyncio
from morceau import Morceau

pygame.init()

class Playlist:
    def __init__(self, nom, id=None):
        self.id = id
        self.nom = nom
        self.morceaux = []
        self.load_morceaux()

    def db_connect(self):
        return Morceau.db_connect()

    def save(self):
        conn = self.db_connect()
        cursor = conn.cursor()
        if not self.id:
            cursor.execute("INSERT INTO playlists (nom, morceau_id, ordre) VALUES (%s, NULL, NULL)", (self.nom,))
            self.id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()

    def load_morceaux(self):
        self.morceaux = []
        conn = self.db_connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT morceau_id, ordre FROM playlists WHERE nom=%s AND morceau_id IS NOT NULL ORDER BY ordre", (self.nom,))
        for row in cursor.fetchall():
            morceau = Morceau.get_by_id(row['morceau_id'])
            if morceau:
                self.morceaux.append(morceau)
        cursor.close()
        conn.close()

    def ajouter_morceau(self, morceau):
        morceau.save()
        self.morceaux.append(morceau)
        self.update_db()

    def supprimer_morceau(self, index):
        if 0 <= index < len(self.morceaux):
            morceau = self.morceaux.pop(index)
            self.update_db()
            return morceau
        return None

    def reorganiser(self, old_index, new_index):
        if 0 <= old_index < len(self.morceaux) and 0 <= new_index < len(self.morceaux):
            morceau = self.morceaux.pop(old_index)
            self.morceaux.insert(new_index, morceau)
            self.update_db()

    def update_db(self):
        conn = self.db_connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM playlists WHERE nom=%s AND morceau_id IS NOT NULL", (self.nom,))
        for i, morceau in enumerate(self.morceaux):
            cursor.execute("INSERT INTO playlists (nom, morceau_id, ordre) VALUES (%s, %s, %s)",
                           (self.nom, morceau.id, i))
        conn.commit()
        cursor.close()
        conn.close()

    async def jouer(self):
        for morceau in self.morceaux:
            print(f"Lecture de {morceau.titre} - {morceau.artiste}")  # Simulé pour Pyodide
            # Pour local: pygame.mixer.music.load(morceau.chemin_fichier)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(1.0 / 60)
            await asyncio.sleep(0.1)