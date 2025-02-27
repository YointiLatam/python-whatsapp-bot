import logging
import os
from app import app  # Asegúrate de que `app` está bien definido en `app/__init__.py`

logging.info("Flask app started")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Render asigna automáticamente el puerto
    app.run(host="0.0.0.0", port=port)


    #iniciar ngrok
    #shell
    #ngrok http 8000 --url snail-deciding-phoenix.ngrok-free.app
