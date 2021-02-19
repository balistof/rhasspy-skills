import dialog
import requests
from rhasspyhermes.nlu import NluIntent


@dialog.app.on_intent("GetWeather")
async def get_weather(intent: NluIntent):
    print("GetWeather")
    try:
        condition_request = requests.get("http://192.168.0.129:8080/rest/items/localCurrentCondition")
        temperature_request = requests.get("http://192.168.0.129:8080/rest/items/localCurrentTemperature")
        result = "es ist {} bei {}".format(condition_request.json()["state"], temperature_request.json()["state"])
        return dialog.responseOK(result)
    except Exception as ex:
        return dialog.responseError(ex)


