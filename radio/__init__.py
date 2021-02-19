import dialog
import requests
from rhasspyhermes.nlu import NluIntent


@dialog.app.on_intent("RadioOnOff")
async def radio_on_off(intent: NluIntent):
    print("RadioOnOff")
    if len(intent.slots) == 0 or intent.slots[0].slot_name != "ein_aus":
        return dialog.EndSession(f"du kannst den radio entweder ein oder aus schalten")

    on_off = "PowerOn"
    if intent.slots[0].value["value"] == "aus":
        on_off = "PowerStandby"
    url = "http://192.168.0.213/goform/formiPhoneAppPower.xml?1+{}".format(on_off)
    response = requests.get(url)
    if response.ok:
        return dialog.responseOK()
    else:
        return dialog.responseError()


@dialog.app.on_intent("RadioVolume")
async def radio_volume(intent: NluIntent):
    print("RadioVolume")
    if len(intent.slots) == 0 or intent.slots[0].slot_name != "volume":
        return dialog.EndSession(f"du kannst den radio entweder lauter oder leiser schalten")

    volume = "MVUP"
    if intent.slots[0].value["value"] == "leiser":
        volume = "MVDOWN"
    url = "http://192.168.0.213/goform/formiPhoneAppDirect.xml?{}".format(volume)
    response = requests.get(url)
    if response.ok:
        return dialog.responseOK()
    else:
        return dialog.responseError()


@dialog.app.on_intent("SetRadioFavorite")
async def radio_favorite(intent: NluIntent):
    print("SetRadioFavorite")
    if len(intent.slots) == 0 or intent.slots[0].slot_name != "favorite":
        return dialog.EndSession(f"du mußt einen kanal angeben")

    channel = intent.slots[0].value["value"]
    url = "http://192.168.0.213/goform/formiPhoneAppDirect.xml?FV%20{:02d}".format(channel)
    response = requests.get(url)
    if response.ok:
        return dialog.responseOK()
    else:
        return dialog.responseError()


