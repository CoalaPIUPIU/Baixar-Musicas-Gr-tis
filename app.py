from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route("/baixar", methods=["POST"])
def baixar():
    # Pega o JSON enviado pelo frontend ou pelo curl
    data = request.get_json()
    nome_musica = data.get("nome")
    
    if not nome_musica:
        return {"erro": "Nenhuma música informada"}, 400

    # Configuração do yt_dlp para baixar MP3
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',  # salva com nome do vídeo
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    # Baixa a música do YouTube
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{nome_musica}", download=True)
        arquivo = ydl.prepare_filename(info)
        arquivo = os.path.splitext(arquivo)[0] + ".mp3"

    # Retorna o arquivo MP3 para download
    return send_file(arquivo, as_attachment=True)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

