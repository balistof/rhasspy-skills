import requests
from rhasspyhermes.nlu import NluIntent

import dialog


@dialog.app.on_intent("Shutters")
async def shutters(intent: NluIntent):
    print("Shutters")
    try:
        allowed_slots = ["shutter_name", "direction"]
        if len(intent.slots) < 2 or intent.slots[0].slot_name not in allowed_slots or \
                intent.slots[1].slot_name not in allowed_slots:
            return dialog.responseError()

        slot1 = intent.slots[0]
        slot2 = intent.slots[1]
        shutter_name = ""
        direction = ""
        if slot1.slot_name == "shutter_name":
            shutter_name = slot1.value["value"]
        else:
            direction = slot1.value["value"]

        if slot2.slot_name == "shutter_name":
            shutter_name = slot2.value["value"]
        else:
            direction = slot2.value["value"]

        direction = direction.upper()
        shutter_map = {"büro": ["Shutter_Buero_Fenster", "Shutter_Buero_Tuer"],
                       "schlafzimmer": ["Shutter_Schlafzimmer"],
                       "kinderzimmer": ["Shutter_Kinder"], "vorraum": ["Shutter_Vorraum"],
                       "wohnzimmer": ["Shutter_Wohnen_FensterGross", "Shutter_Wohnen_TuerRechts"]}
        matching_shutters = shutter_map.get(shutter_name, None)
        if matching_shutters is None:
            dialog.responseError()
        headers = {"Content-Type": "text/plain"}
        for shutter in matching_shutters:
            requests.post("http://192.168.0.129:8080/rest/items/" + shutter, data=direction, headers=headers)
        return dialog.responseOK()
    except Exception as ex:
        return dialog.responseError(ex)


