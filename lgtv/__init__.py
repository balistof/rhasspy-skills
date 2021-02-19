from rhasspyhermes.nlu import NluIntent

import dialog
from lgtv import lg


@dialog.app.on_intent("LGTVOff")
async def lg_tv_off(intent: NluIntent):
    print("LGTVOff")
    try:
        address = lg.Remote.find_tvs(first_only=True)
        remote = lg.Remote(address)
        remote.set_pairing_key("394905")
        remote.send_command(lg.Remote.POWER)
        return dialog.responseOK()
    except Exception as ex:
        return dialog.responseError(ex)


@dialog.app.on_intent("LGTVChannel")
async def lg_tv_channel(intent: NluIntent):
    print("LGTVChannel")
    try:
        if len(intent.slots) == 0 or intent.slots[0].slot_name != "channel":
            return dialog.responseError(f"du mußt einen kanal angeben")
        channel = str(intent.slots[0].value["value"])
        address = lg.Remote.find_tvs(first_only=True)
        remote = lg.Remote(address)
        remote.set_pairing_key("394905")

        commands = []
        for digit in channel:
            commands.append(int(digit) + 2)
        remote.send_multiple(commands)
        return dialog.responseOK()
    except Exception as ex:
        return dialog.responseError(ex)



