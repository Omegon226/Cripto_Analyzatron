from view.view_fear_and_greed_data import ViewFeatAndGreedData
import requests
import json
import re


class ControllerFeatAndGreedData:
    @staticmethod
    def fear_and_greed_data(message, **kwargs):
        query = re.findall(r"\D+ ([\d]+)", message.text)[0]

        kwargs["data"] = ControllerFeatAndGreedData.__get_data_from_request(int(query))
        ViewFeatAndGreedData.fear_and_greed_data(message, **kwargs)

    @staticmethod
    def __get_data_from_request(period=90):
        url = "https://api.alternative.me/fng/?limit=0"
        response = requests.get(url)
        response_data = json.loads(response.text)

        aggregated_data = {
            "data": response_data["data"][:period],
            "period_days": period
        }

        return aggregated_data
