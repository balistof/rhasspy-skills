"""Example app to react to an intent to tell you the time."""
import logging
from datetime import datetime

from rhasspyhermes.nlu import NluIntent, NluIntentNotRecognized

from rhasspyhermes_app import EndSession, HermesApp

_LOGGER = logging.getLogger("BaseApp")

app = HermesApp("BaseApp")

@app.on_intent("GetTime")
async def get_time(intent: NluIntent):
    """Tell the time."""
    now = datetime.now().strftime("%H Uhr %M")
    return EndSession(f"Es ist {now}")

@app.on_intent("GetWeather")
async def get_time(intent: NluIntent):
    return EndSession(f"das wetter kenn ich noch nicht")

@app.on_intent_not_recognized
async def not_understood(intent_not_recognized: NluIntentNotRecognized):
    return EndSession(f"tut mir leid das muß ich erst lernen")

app.run()
