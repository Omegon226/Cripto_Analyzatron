from view.view_stacking import ViewStacking
import requests
import re


class ControllerStacking:
    @staticmethod
    def stacking_info(message, **kwargs):
        try:
            query = re.findall(r"\D+ ([\w]+)", message.text)[0]
            kwargs["bot"].logger.info(f'Начало stacking_info с запросом {query}')
            kwargs["data"] = ControllerStacking.__get_data_from_request(kwargs["bot"].stakingrewards_token, query)
        except:
            kwargs["bot"].logger.info(f'Начало stacking_info с запросом {"polkadot"}')
            kwargs["data"] = ControllerStacking.__get_data_from_request(kwargs["bot"].stakingrewards_token, "polkadot")
        ViewStacking.stacking_info(message, **kwargs)

    @staticmethod
    def __get_data_from_request(stakingrewards_token, iso):
        endpoint = "https://api.stakingrewards.com/public/query"
        query = '''
        query Step1 {
            assets(where: { symbols: ["''' + iso + '''"] }, limit: 1) {
                id
                slug
                logoUrl
                metrics(
                    where: { metricKeys: ["reward_rate"]}
                    limit: 1
                    order: { createdAt: desc }
                ) {
                    defaultValue
                    createdAt
                }
            }
        }
        '''
        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": stakingrewards_token,
        }
        stakingrewards_response_1 = requests.post(endpoint, json={"query": query}, headers=headers)
        stakingrewards_response_1_data = stakingrewards_response_1.json()
        if stakingrewards_response_1_data == []:
            return {"error": "Не удалось получить данные из запроса"}

        endpoint = "https://api.stakingrewards.com/public/query"
        query = '''
        query Step2 {
            providers(
                where: {rewardOptions: {inputAsset: {symbols: ["''' + iso + '''"]},}, isVerified: true}
                order: {metricKey_desc: "assets_under_management"}
                limit: 10
            ) {
                slug
                rewardOptions(
                  where: {inputAsset: {symbols: ["''' + iso + '''"]}}
                  limit: 1
                ) {
                    metrics(
                        where: {metricKeys: ["reward_rate"]}
                        limit: 1
                    ) {
                        defaultValue
                    }
                }
            }
        }
        '''

        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": stakingrewards_token,
        }
        stakingrewards_response_2 = requests.post(endpoint, json={"query": query}, headers=headers)
        stakingrewards_response_2_data = stakingrewards_response_2.json()
        if stakingrewards_response_2_data == []:
            return {"error": "Не удалось получить данные из запроса"}

        stacking_providers = []

        for provider in stakingrewards_response_2_data["data"]["providers"]:
            if provider['rewardOptions'] is not None:
                if provider['rewardOptions'][0]["metrics"] is not None:
                    stacking_providers += [provider]

        aggregated_data = {
            "name": stakingrewards_response_1_data["data"]["assets"][0]["slug"],
            "apr": stakingrewards_response_1_data["data"]["assets"][0]["metrics"][0]["defaultValue"],
            "providers": stacking_providers
        }

        return aggregated_data


