from view.view_fear_and_greed_data import ViewFeatAndGreedData
import requests
import json
import re


class ControllerFeatAndGreedData:
    @staticmethod
    def fear_and_greed_data(message, **kwargs):
        try:
            query = re.findall(r"\D+ ([\d]+)", message.text)[0]
            kwargs["bot"].logger.info(f'Начало fear_and_greed_data с запросом {query}')
            kwargs["data"] = ControllerFeatAndGreedData.__get_data_from_request(int(query))
        except:
            kwargs["bot"].logger.info(f'Начало fear_and_greed_data с запросом {90}')
            kwargs["data"] = ControllerFeatAndGreedData.__get_data_from_request()
        ViewFeatAndGreedData.fear_and_greed_data(message, **kwargs)

    @staticmethod
    def __get_data_from_request(period=90):
        url = "https://api.alternative.me/fng/?limit=0"
        response = requests.get(url)
        if response not in [200, 300]:
            return {"error": "Не удалось получить данные из запроса"}

        response_data = json.loads(response.text)

        aggregated_data = {
            "data": response_data["data"][:period],
            "period_days": period
        }

        return aggregated_data
