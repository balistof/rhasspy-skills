import requests
from rhasspyhermes.nlu import NluIntent

import dialog


@dialog.app.on_intent("VacuumStart")
async def shutters(intent: NluIntent):
    print("VacuumStart")
    try:
        # todo: call openhab
        # set item vacuum state to start
        #headers = {"Content-Type": "text/plain"}
        #requests.post("http://192.168.0.129:8080/rest/items/" + shutter, data=direction, headers=headers)
        return dialog.responseOK("das muß mir christoph ers beibringen")
    except Exception as ex:
        return dialog.responseError(ex)


