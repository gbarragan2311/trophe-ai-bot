
from msgraph import get_token, get_emails, get_events
from transformers import pipeline

summarizer = pipeline("summarization")

async def handle_message(text: str) -> str:
    text = text.lower()
    token = get_token()

    if "correo" in text:
        emails = get_emails(token)
        if not emails:
            return "No encontré correos recientes 📭"
        body = emails[0]["body"]["content"][:1000]
        resumen = summarizer(body, max_length=60, min_length=20, do_sample=False)[0]["summary_text"]
        return f"📬 Resumen de tu correo:\n\n{resumen}"

    elif "reunión" in text or "calendario" in text:
        eventos = get_events(token)
        if not eventos:
            return "No tienes reuniones hoy 🎉"
        detalles = "\n".join(f"- {e['subject']} a las {e['start']['dateTime']}" for e in eventos)
        return f"📅 Reuniones de hoy:\n\n{detalles}"

    return "👋 Hola, soy tu asistente. Puedes decir 'resumen de correo' o 'mis reuniones'."
