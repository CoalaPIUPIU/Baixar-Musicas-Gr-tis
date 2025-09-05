import time
from flask import Flask, request, send_file
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)  # Permite requisições de qualquer origem

@app.route("/baixar", methods=["POST"])
def baixar():
    data = request.get_json()
    nome_musica = data.get("nome")
    
    if not nome_musica:
        return {"erro": "Nenhuma música informada"}, 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # salva na pasta downloads
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    os.makedirs("downloads", exist_ok=True)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{nome_musica}", download=True)
        arquivo = ydl.prepare_filename(info)
        arquivo = os.path.splitext(arquivo)[0] + ".mp3"

    # Pequena espera para garantir que o arquivo esteja pronto
    time.sleep(2)

    return send_file(arquivo, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
