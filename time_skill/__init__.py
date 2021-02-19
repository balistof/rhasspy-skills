from datetime import datetime

from rhasspyhermes.nlu import NluIntent

import dialog


@dialog.app.on_intent("GetTime")
async def get_time(intent: NluIntent):
    print("GetTime")
    now = datetime.now().strftime("%-H Uhr %-M")
    return dialog.responseOK(f"Es ist {now}")

