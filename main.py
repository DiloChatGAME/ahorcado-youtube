# main.py

from flask import Flask, render_template
from game import GameManager
import pytchat
import threading
import time

app = Flask(__name__)
game = GameManager()

# 👉 Añade aquí el ID de tu vídeo en directo de YouTube
YOUTUBE_VIDEO_ID = "PON_AQUI_EL_ID_DEL_VIDEO"

# Intervalo entre turnos en segundos
TURNO_SEGUNDOS = 30

def leer_chat():
    chat = pytchat.create(video_id=YOUTUBE_VIDEO_ID)
    while chat.is_alive():
        for c in chat.get().sync_items():
            msg = c.message.lower().strip()
            autor = c.author.name
            if msg.startswith("/letra "):
                letra = msg.replace("/letra", "").strip()
                if len(letra) == 1 and letra.isalpha():
                    game.vote_letter(autor, letra)
            elif msg.startswith("/palabra "):
                palabra = msg.replace("/palabra", "").strip()
                if palabra.isalpha():
                    game.vote_word(autor, palabra)
        time.sleep(1)

def bucle_juego():
    while True:
        time.sleep(TURNO_SEGUNDOS)
        if not game.finished:
            game.check_word_guesses()
            game.apply_voted_letter()
        else:
            time.sleep(10)
            game.reset_game()

@app.route("/")
def index():
    return render_template("juego.html", 
                           palabra=game.get_visible_word(), 
                           fallos=game.fails, 
                           mensaje=game.result_message, 
                           marcador=game.get_scores())

# Iniciar hilos paralelos
threading.Thread(target=leer_chat, daemon=True).start()
threading.Thread(target=bucle_juego, daemon=True).start()

# Lanzar servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
