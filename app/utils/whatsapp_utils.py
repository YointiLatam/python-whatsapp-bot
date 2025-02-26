import logging
from flask import current_app, jsonify
import json
import requests
from app.services.openai_service import generate_response
import re


def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )


def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(url, json=json.loads(data), headers=headers, timeout=10)
        response.raise_for_status()
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        log_http_response(response)
        return response


def process_text_for_whatsapp(text):
    """Format the text to WhatsApp style"""
    text = re.sub(r"\【.*?\】", "", text).strip()
    return re.sub(r"\*\*(.*?)\*\*", r"*\1*", text)


def process_whatsapp_message(body):
    """
    Process an incoming WhatsApp message, generate a response, and send it back.
    """
    try:
        changes = body["entry"][0]["changes"][0]["value"]
        wa_id = changes["contacts"][0]["wa_id"]
        name = changes["contacts"][0]["profile"]["name"]
        message_body = changes["messages"][0]["text"]["body"]

        print(f"Hola {name}")

        # Generate response using OpenAI
        response = generate_response(message_body, wa_id, name)
        response = process_text_for_whatsapp(response)

        data = get_text_message_input(wa_id, response)
        send_message(data)

    except KeyError as e:
        logging.error(f"Error processing WhatsApp message: {e}")


def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    try:
        return (
            body.get("object") == "whatsapp_business_account"
            and "entry" in body
            and "changes" in body["entry"][0]
            and "value" in body["entry"][0]["changes"][0]
            and "messages" in body["entry"][0]["changes"][0]["value"]
        )
    except (IndexError, KeyError, TypeError):
        return False
