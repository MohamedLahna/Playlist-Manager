import tkinter as tk
import asyncio
import platform
from morceau import Morceau
from playlist import Playlist
from playlistapp import PlaylistApp

async def main():
    playlist = Playlist("Ma Playlist")
    playlist.ajouter_morceau(Morceau("Chanson 1", "Artiste 1", "chanson1.mp3"))
    playlist.ajouter_morceau(Morceau("Chanson 2", "Artiste 2", "chanson2.mp3"))
    playlist.save()

    root = tk.Tk()
    app = PlaylistApp(root, playlist)
    root.update()
    
    while True:
        try:
            root.update()
            await asyncio.sleep(1.0 / 60)
        except tk.TclError:
            break

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())