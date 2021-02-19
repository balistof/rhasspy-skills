import dialog
import feedparser
import random
from rhasspyhermes.nlu import NluIntent
from io import StringIO
from html.parser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

@dialog.app.on_intent("News")
async def news(intent: NluIntent):
    print("News")
    try:
        #news_feed = feedparser.parse("https://rss.orf.at/oe3.xml")
        news_feed = feedparser.parse("https://www.derstandard.at/rss")
        news = []
        for entry in news_feed["entries"]:
            if "/sendungen/" in entry["link"]:
                continue
            news.append(entry)

        news_text = "die schlagzeilen lauten. "
        for entry in random.sample(news, 3):
            news_text += entry["title"] + ". " + strip_tags(entry["description"]) + ". . "

        return dialog.responseOK(news_text)
    except Exception as ex:
        return dialog.responseError(ex)


