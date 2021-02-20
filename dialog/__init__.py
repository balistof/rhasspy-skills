from rhasspyhermes.nlu import NluIntentNotRecognized
from rhasspyhermes_app import EndSession, HermesApp
import random

ok_messages = ["ok", "alles klar", "mach ich", "gerne", "kommt sofort", "bitteschön", "wird gemacht"]

app = HermesApp("main")


@app.on_intent_not_recognized
async def not_understood(intent_not_recognized: NluIntentNotRecognized):
    return EndSession(f"tut mir leid das muß ich erst lernen")


def run():
    app.run()


def responseOK(response=None):
    if response is None:
        return EndSession(random.choice(ok_messages))
    else:
        print("RESPONSE: " + response)
        return EndSession(response)


def responseError(error=None):
    print("ERROR", error)
    return EndSession(f"da ist leider ein fehler aufgetreten")
