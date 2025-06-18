
# TrophA - Bot Inteligente para Teams

Este bot permite consultar correos y reuniones desde Microsoft Teams usando Graph API y FastAPI.

## Instalación
1. Clona el repo
2. Crea un `.env` con CLIENT_ID y TENANT_ID
3. Ejecuta:
```
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
ngrok http 8000
```

## Funcionalidad
- "Resumen de correo"
- "Mis reuniones"
