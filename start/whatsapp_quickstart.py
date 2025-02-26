import json
from dotenv import load_dotenv
import os
import requests
import aiohttp
import asyncio

# --------------------------------------------------------------
# Load environment variables
# --------------------------------------------------------------
load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")

# --------------------------------------------------------------
# COMENTADO: Esta función envía el mensaje "hello_world" (MENSAJE AUTOMÁTICO)
# --------------------------------------------------------------
# def send_whatsapp_message():
#     url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
#     headers = {
#         "Authorization": "Bearer " + ACCESS_TOKEN,
#         "Content-Type": "application/json",
#     }
#     data = {
#         "messaging_product": "whatsapp",
#         "to": RECIPIENT_WAID,
#         "type": "template",
#         "template": {"name": "hello_world", "language": {"code": "en_US"}},
#     }
#     response = requests.post(url, headers=headers, json=data)
#     return response

# COMENTADO: Se eliminó la línea que ejecuta el mensaje automático
# response = send_whatsapp_message()
# print(response.status_code)
# print(response.json())

# --------------------------------------------------------------
# Send a custom text WhatsApp message asynchronously
# --------------------------------------------------------------


async def send_message_async(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    async with aiohttp.ClientSession() as session:
        url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
        try:
            async with session.post(url, data=data, headers=headers) as response:
                if response.status == 200:
                    print("Status:", response.status)
                    print("Content-type:", response.headers["content-type"])
                    html = await response.text()
                    print("Body:", html)
                else:
                    print(response.status)
                    print(await response.text())  # Muestra el error exacto
        except aiohttp.ClientConnectorError as e:
            print("Connection Error", str(e))
        finally:
            await session.close()  # Cierra la sesión


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,  # Asegúrate que aquí va el wa_id dinámico
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )


async def main(wa_id, user_name):
    data = get_text_message_input(
        recipient=wa_id,  # ✅ Número dinámico del usuario
        text=f"👋 ¡Hola {user_name}! Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?" #funciona para hacer pruebas
    )
    await send_message_async(data)



if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
