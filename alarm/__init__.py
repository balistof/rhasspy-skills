import json
import threading
import uuid
from datetime import datetime, timedelta

from rhasspyhermes.nlu import NluIntent
from rhasspyhermes_app import ContinueSession

import dialog

alarm_state_file = "alarm_state.data"

session_store = dict()


def alarm_timer():
    try:
        expired_entries = {}
        with open(alarm_state_file, 'r') as file:
            data = json.load(file)
            for entry in data:
                expiry = datetime.strptime(entry["dateTime"], "%Y-%m-%d %H:%M")
                if expiry <= datetime.now():
                    entry["expiry"] = expiry
                    expired_entries[entry["id"]] = entry

        for entry_id, expired_entry in expired_entries.items():
            expiry = expired_entry["expiry"]
            dialog.app.notify("hallo, ich sollte dich um {} erinnern".format(expiry.strftime("%-H Uhr %-M")),
                       expired_entry["siteId"])

        if len(expired_entries) != 0:
            data = [entry for entry in data if entry["id"] not in expired_entries.keys()]
            with open(alarm_state_file, 'w') as file:
                json.dump(data, file)

    except Exception as ex:
        print("ERROR alarms state", ex)
    finally:
        threading.Timer(1, alarm_timer).start()


alarm_timer()


@dialog.app.on_intent("Alarm")
async def alarm(intent: NluIntent):
    print("Alarm")
    try:
        allowed_slots = ["unit", "delay", "hour", "minute"]
        if len(intent.slots) < 2 or intent.slots[0].slot_name not in allowed_slots or \
                intent.slots[1].slot_name not in allowed_slots:
            return dialog.responseError()
        slot1 = intent.slots[0]
        slot2 = intent.slots[1]
        alarm_date_time = datetime.now()
        if slot1.slot_name == "delay":
            delay = slot1.value["value"]
            unit_raw = str(slot2.value["value"]).lower()
            if "minute" in unit_raw:
                alarm_date_time += timedelta(minutes=delay)
            elif "stunde" in unit_raw:
                alarm_date_time += timedelta(hours=delay)
            else:
                return dialog.responseError()
        else:
            hour = slot1.value["value"]
            minute = slot2.value["value"]
            alarm_date_time = alarm_date_time.replace(hour=hour, minute=minute)

        result = ContinueSession()
        result.text = "ich setze einen alarm für {} . ist das richtig?".format(alarm_date_time.strftime("%-H Uhr %-M"))
        result.intent_filter = ["Confirmation"]
        result.custom_data = json.dumps({"intent": "alarm",
                                         "data": {"siteId": intent.site_id,
                                                  "id": uuid.uuid4().hex,
                                                  "dateTime": alarm_date_time.strftime("%Y-%m-%d %H:%M")}})
        session_store[intent.session_id] = result.custom_data

        return result
    except Exception as ex:
        return dialog.responseError(ex)


@dialog.app.on_intent("Confirmation")
async def confirmation(intent: NluIntent):
    print("Confirmation")
    try:
        session_data_raw = session_store.pop(intent.session_id, None)
        if session_data_raw is None or len(intent.slots) < 1:
            return dialog.responseError()

        if intent.slots[0].value["value"] == "dismiss":
            return dialog.responseOK()

        session_data = json.loads(session_data_raw)
        payload = session_data.get("data", None)
        if session_data.get("intent", None) == "alarm" and payload is not None:
            try:
                with open(alarm_state_file, 'r') as file:
                    data = json.load(file)
            except:
                data = None
            if data is None:
                data = []
            data.append(payload)
            with open(alarm_state_file, 'w') as file:
                json.dump(data, file)

            return dialog.responseOK("alarm für {} ist gesetzt".format(
                datetime.strptime(payload["dateTime"], "%Y-%m-%d %H:%M").strftime("%-H Uhr %-M")))

        return dialog.responseOK("das muß der Christoph mir erst beibringen")
    except Exception as ex:
        return dialog.responseError(ex)

