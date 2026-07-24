import mysql.connector
from mysql.connector import Error

class Morceau:
    def __init__(self, titre, artiste, chemin_fichier, id=None):
        self.id = id
        self.titre = titre
        self.artiste = artiste
        self.chemin_fichier = chemin_fichier

    def afficher(self):
        return f"{self.titre} - {self.artiste}"

    @staticmethod
    def db_connect():
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",  # Remplacez par votre utilisateur MySQL
                password="",  # Remplacez par votre mot de passe
                database="playlist_db"
            )
            return conn
        except Error as e:
            print(f"Erreur de connexion à MySQL: {e}")
            return None

    def save(self):
        conn = self.db_connect()
        if conn is None:
            return False
            
        cursor = conn.cursor()
        try:
            if self.id:
                cursor.execute(
                    "UPDATE morceaux SET titre=%s, artiste=%s, chemin_fichier=%s WHERE id=%s",
                    (self.titre, self.artiste, self.chemin_fichier, self.id)
                )
            else:
                cursor.execute(
                    "INSERT INTO morceaux (titre, artiste, chemin_fichier) VALUES (%s, %s, %s)",
                    (self.titre, self.artiste, self.chemin_fichier)
                )
                self.id = cursor.lastrowid
            conn.commit()
            return True
        except Error as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_id(morceau_id):
        conn = Morceau.db_connect()
        if conn is None:
            return None
            
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM morceaux WHERE id=%s", (morceau_id,))
            result = cursor.fetchone()
            if result:
                return Morceau(
                    result['titre'],
                    result['artiste'],
                    result['chemin_fichier'],
                    result['id']
                )
            return None
        except Error as e:
            print(f"Erreur lors de la récupération: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all():
        conn = Morceau.db_connect()
        if conn is None:
            return []
            
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM morceaux ORDER BY titre")
            return [
                Morceau(
                    row['titre'],
                    row['artiste'],
                    row['chemin_fichier'],
                    row['id']
                ) for row in cursor.fetchall()
            ]
        except Error as e:
            print(f"Erreur lors de la récupération: {e}")
            return []
        finally:
            cursor.close()
            conn.close()