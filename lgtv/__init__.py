from rhasspyhermes.nlu import NluIntent

import dialog
from lgtv import lg


@dialog.app.on_intent("LGTVOff")
async def lg_tv_off(intent: NluIntent):
    print("LGTVOff")
    try:
        remote = lg.Remote("192.168.0.178", "394905")
        remote.send_command(lg.Remote.POWER)
        return dialog.responseOK("")
    except Exception as ex:
        return dialog.responseError(ex)


@dialog.app.on_intent("LGTVChannel")
async def lg_tv_channel(intent: NluIntent):
    print("LGTVChannel")
    try:
        if len(intent.slots) == 0 or intent.slots[0].slot_name != "channel":
            return dialog.responseError(f"du mußt einen kanal angeben")
        channel = str(intent.slots[0].value["value"])
        remote = lg.Remote("192.168.0.178", "394905")
        commands = []
        for digit in channel:
            commands.append(int(digit) + 2)
        remote.send_multiple(commands)
        return dialog.responseOK("")
    except Exception as ex:
        return dialog.responseError(ex)


@dialog.app.on_intent("LGTVVolume")
async def lg_tv_channel(intent: NluIntent):
    print("LGTVVolume")
    try:
        if len(intent.slots) == 0 or intent.slots[0].slot_name != "volume":
            return dialog.responseError()
        remote = lg.Remote("192.168.0.178", "394905")
        if intent.slots[0].value["value"] == "lauter":
            command = lg.Remote.VOLUME_UP
        else:
            command = lg.Remote.VOLUME_DOWN
        remote.send_command(command)
        return dialog.responseOK("")
    except Exception as ex:
        return dialog.responseError(ex)

