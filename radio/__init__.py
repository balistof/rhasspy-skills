import dialog
import requests
import mopidyapi
from rhasspyhermes.nlu import NluIntent
import time

mopidy = mopidyapi.MopidyAPI(host='192.168.0.157', use_websocket=False)

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
    mopidy.tracklist.clear()
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

@dialog.app.on_intent("PlayInternetRadio")
async def radio_mopidy(intent: NluIntent):
    print("PlayInternetRadio")
    if len(intent.slots) == 0 or intent.slots[0].slot_name != "station":
        return dialog.EndSession(f"du mußt einen kanal angeben")

    channel = intent.slots[0].value["value"]
    if channel == "ö 3":
        mopidy_uri = "tunein:station:s8007"
    elif channel == "krone hit":
        mopidy_uri = "tunein:station:s218146"
    elif channel == "kinder radio":
        mopidy_uri = "tunein:station:s267651"
    elif channel == "fm 4":
        mopidy_uri = "tunein:station:s8235"
    elif channel == "radio osttirol":
        mopidy_uri = "tunein:station:s15545"
    else:
        return dialog.responseOK("den kanal {} kenne ich nicht".format(channel))

    # first switch radio on; if needed
    status_url = "http://192.168.0.213/goform/formMainZone_MainZoneXml.xml"
    response = requests.get(status_url)
    if "<Power><value>STANDBY</value></Power>" in response.text:
        if not requests.get("http://192.168.0.213/goform/formiPhoneAppPower.xml?1+PowerOn").ok:
            return dialog.responseError()
        time.sleep(5)

    # then set to aux in
    url = "http://192.168.0.213/goform/formiPhoneAppDirect.xml?SIANALOGIN"
    response = requests.get(url)
    if not response.ok:
        return dialog.responseError()

    # finally use the station name to switch to it
    mopidy.tracklist.clear()
    mopidy.tracklist.add(uris=[mopidy_uri])
    mopidy.playback.play(tlid=1)
    return dialog.responseOK()

@dialog.app.on_intent("RadioCurrentlyPlayed")
async def radio_mopidy(intent: NluIntent):
    print("RadioCurrentlyPlayed")

    state = mopidy.playback.get_state()
    if state == "playing":
        title = mopidy.playback.get_current_track().album.name.lower()
        stream_title = mopidy.playback.get_stream_title()
        if stream_title is not None:
            stream_title = stream_title.lower()
            if title not in stream_title and "adbreak" not in stream_title:
                title += " - " + mopidy.playback.get_stream_title()
        return dialog.responseOK("es läuft {}".format(title))
    else:
        return dialog.responseOK("ich spiele gerade nichts")

