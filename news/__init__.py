import dialog
import feedparser
from rhasspyhermes.nlu import NluIntent


@dialog.app.on_intent("News")
async def news(intent: NluIntent):
    print("News")
    try:
        # news_feed = feedparser.parse("https://rss.orf.at/news.xml")
        news_feed = feedparser.parse("https://rss.orf.at/oe3.xml")
        news_text = "die schlagzeilen lauten. "
        max_entries = 3
        i = 0
        for entry in news_feed["entries"]:
            if i >= max_entries:
                break
            if "/sendungen/" in entry["link"]:
                continue
            news_text += entry["title"] + ". " + entry["description"] + ". . "
            i += 1
        return dialog.responseOK(news_text)
    except Exception as ex:
        return dialog.responseError(ex)


