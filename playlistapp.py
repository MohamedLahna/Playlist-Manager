import tkinter as tk
from tkinter import ttk, messagebox

class PlaylistApp:
    def __init__(self, root, playlist):
        self.root = root
        self.root.title("Organisateur de Playlists")
        self.playlist = playlist

        self.frame = ttk.Frame(self.root).pack(padx=10, pady=10)
        self.listbox = tk.Listbox(self.frame, width=50, height=10)
        self.listbox.pack(pady=5)
        self.listbox.bind('<Button-1>', self.start_drag)
        self.listbox.bind('<ButtonRelease-1>', self.drop)

        ttk.Button(self.frame, text="Ajouter", command=self.ajouter_morceau).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.frame, text="Supprimer", command=self.supprimer_morceau).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.frame, text="Jouer", command=self.jouer_playlist).pack(side=tk.LEFT, padx=5)

        self.drag_start_index = None
        self.mettre_a_jour_listbox()

    def mettre_a_jour_listbox(self):
        self.listbox.delete(0, tk.END)
        for morceau in self.playlist.morceaux:
            self.listbox.insert(tk.END, morceau.afficher())

    def ajouter_morceau(self):
        titre = f"Chanson {len(self.playlist.morceaux) + 1}"
        artiste = f"Artiste {len(self.playlist.morceaux) + 1}"
        chemin = f"{titre.lower().replace(' ', '_')}.mp3"
        self.playlist.ajouter_morceau(Morceau(titre, artiste, chemin))
        self.mettre_a_jour_listbox()

    def supprimer_morceau(self):
        try:
            index = self.listbox.curselection()[0]
            self.playlist.supprimer_morceau(index)
            self.mettre_a_jour_listbox()
        except IndexError:
            messagebox.showwarning("Erreur", "Sélectionnez un morceau.")

    def start_drag(self, event):
        self.drag_start_index = self.listbox.nearest(event.y)

    def drop(self, event):
        if self.drag_start_index is not None:
            new_index = self.listbox.nearest(event.y)
            if new_index != self.drag_start_index:
                self.playlist.reorganiser(self.drag_start_index, new_index)
                self.mettre_a_jour_listbox()
            self.drag_start_index = None

    async def jouer_playlist(self):
        await self.playlist.jouer()