import random
import dialog
from rhasspyhermes.nlu import NluIntent


@dialog.app.on_intent("RandomDice")
async def skill_random_dice(intent: NluIntent):
    print("RandomDice")
    try:
        if len(intent.slots) == 0 or intent.slots[0].slot_name != "repeat":
            text = "{}".format(random.randint(1, 6))
        else:
            repeat = intent.slots[0].value["value"]
            text = ""
            for i in range(repeat):
                text += "{} ".format(random.randint(1, 6))
        return dialog.responseOK(text)
    except Exception as ex:
        return dialog.responseError(ex)


@dialog.app.on_intent("RandomNumber")
async def skill_random_number(intent: NluIntent):
    print("RandomNumber")
    try:
        allowed_slots = ["repeat", "start", "end"]
        if len(intent.slots) < 2 or intent.slots[0].slot_name not in allowed_slots or \
                intent.slots[1].slot_name not in allowed_slots:
            return dialog.responseError()
        repeat = 1
        if intent.slots[0].slot_name == "repeat":
            repeat = intent.slots[0].value["value"]
            start = intent.slots[1].value["value"]
            end = intent.slots[2].value["value"]
        else:
            start = intent.slots[0].value["value"]
            end = intent.slots[1].value["value"]

        text = "{} ".format(random.randint(start, end))
        for i in range(1, repeat):
            text += "{} ".format(random.randint(start, end))
        return dialog.responseOK(text)
    except Exception as ex:
        return dialog.responseError(ex)
