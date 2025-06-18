from fastapi import FastAPI, Request
from fastapi.responses import Response
from dotenv import load_dotenv
from botbuilder.schema import Activity
from botbuilder.core import BotFrameworkAdapter, TurnContext, BotFrameworkAdapterSettings
import os
from bot_logic import handle_message

load_dotenv()
app = FastAPI()

APP_ID = os.getenv("CLIENT_ID")
APP_PASSWORD = os.getenv("CLIENT_SECRET")

settings = BotFrameworkAdapterSettings(app_id=APP_ID, app_password=APP_PASSWORD)
adapter = BotFrameworkAdapter(settings)

@app.post("/api/messages")
async def messages(req: Request):
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")

    async def call_bot(turn_context: TurnContext):
        response = await handle_message(activity.text)
        await turn_context.send_activity(response)

    await adapter.process_activity(activity, auth_header, call_bot)
    return Response(status_code=200)
