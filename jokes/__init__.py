import pyjokes
import dialog
from rhasspyhermes.nlu import NluIntent


@dialog.app.on_intent("Joke")
async def joke(intent: NluIntent):
    print("Joke")
    try:
        # feed = feedparser.parse("https://www.hahaha.de/witze/neuestewitze.xml")
        # text = random.choice(feed["entries"])["summary"]
        text = pyjokes.get_joke(language="de")
        return dialog.responseOK(text)
    except Exception as ex:
        return dialog.responseError(ex)


