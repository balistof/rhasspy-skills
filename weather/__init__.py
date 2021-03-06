import dialog
import requests
from rhasspyhermes.nlu import NluIntent


@dialog.app.on_intent("GetWeather")
async def get_weather(intent: NluIntent):
    print("GetWeather")
    try:
        allowed_slots = ["day"]
        if len(intent.slots) < 1 or intent.slots[0].slot_name not in allowed_slots:
            return dialog.responseError()
        day = intent.slots[0].value["value"]
        if "morgen" == day:
            condition_request = requests.get("http://192.168.0.129:8080/rest/items/localTomorrowCondition")
            temperature_min_request = requests.get("http://192.168.0.129:8080/rest/items/localDailyForecastTomorrowMinTemperature")
            temperature_max_request = requests.get("http://192.168.0.129:8080/rest/items/localDailyForecastTomorrowMaxTemperature")
            result = "morgen wird es {} bei temperaturen zwischen {} und {}".format(condition_request.json()["state"],
                                                                                    temperature_min_request.json()["state"],
                                                                                    temperature_max_request.json()["state"])
        elif "übermorgen" == day:
            condition_request = requests.get("http://192.168.0.129:8080/rest/items/localDay2Condition")
            temperature_min_request = requests.get(
                "http://192.168.0.129:8080/rest/items/localDailyForecastDay2MinTemperature")
            temperature_max_request = requests.get(
                "http://192.168.0.129:8080/rest/items/localDailyForecastDay2MaxTemperature")
            result = "übermorgen wird es {} bei temperaturen zwischen {} und {}".format(condition_request.json()["state"],
                                                                                    temperature_min_request.json()[
                                                                                        "state"],
                                                                                    temperature_max_request.json()[
                                                                                        "state"])
        else:
            condition_request = requests.get("http://192.168.0.129:8080/rest/items/localCurrentCondition")
            temperature_request = requests.get("http://192.168.0.129:8080/rest/items/localCurrentTemperature")
            result = "es ist {} bei {}".format(condition_request.json()["state"], temperature_request.json()["state"])

        return dialog.responseOK(result)
    except Exception as ex:
        return dialog.responseError(ex)


