import os
import requests
from msgraph import get_token, get_emails, get_events

def summarize_with_api(text: str) -> str:
    """
    Realiza una solicitud a la API de Hugging Face para generar un resumen.
    El modelo usado es distilbart-cnn-12-6.
    """
    headers = {
        "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
        "Content-Type": "application/json"
    }
    payload = {"inputs": text[:1000]}  # limitar a 1000 caracteres si es necesario
    response = requests.post(
        "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6",
        headers=headers,
        json=payload
    )
    try:
        result = response.json()
        if isinstance(result, list) and "summary_text" in result[0]:
            return result[0]["summary_text"]
        else:
            return "No se pudo generar el resumen del correo."
    except Exception as e:
        return f"Ocurrió un error al resumir el texto: {str(e)}"

async def handle_message(text: str) -> str:
    """
    Lógica principal del bot según el mensaje recibido.
    """
    text = text.lower()
    token = get_token()

    if "correo" in text:
        emails = get_emails(token)
        if not emails:
            return "No encontré correos recientes 📭"

        body = emails[0]["body"]["content"]
        resumen = summarize_with_api(body)
        return f"📬 Resumen de tu correo:\n\n{resumen}"

    elif "reunión" in text or "calendario" in text:
        eventos = get_events(token)
        if not eventos:
            return "No tienes reuniones hoy 🎉"
        detalles = "\n".join(f"- {e['subject']} a las {e['start']['dateTime']}" for e in eventos)
        return f"📅 Reuniones de hoy:\n\n{detalles}"

    return "👋 Hola, soy tu asistente. Puedes decir 'resumen de correo' o 'mis reuniones'."
