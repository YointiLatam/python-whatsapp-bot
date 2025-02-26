import logging

from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    logging.info("Flask app started")
    app.run(host=os.getenv("HOST"), port=os.getenv("PORT", 8080))

    #iniciar ngrok
    #shell
    #ngrok http 8000 --url snail-deciding-phoenix.ngrok-free.app
