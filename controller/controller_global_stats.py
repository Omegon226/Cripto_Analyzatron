from view.view_global_stats import ViewGlobalStats
import requests
import json
import re


class ControllerGlobalStats:
    @staticmethod
    def global_stats(message, **kwargs):
        kwargs["bot"].logger.info(f'Начало global_stats')
        kwargs["data"] = ControllerGlobalStats.__get_data_for_global_stats(kwargs["bot"].coinmarketcap_token)
        ViewGlobalStats.global_stats(message, **kwargs)

    @staticmethod
    def top_coins(message, **kwargs):
        try:
            query = re.findall(r"\D+ ([\d]+)", message.text)[0]
            kwargs["bot"].logger.info(f'Начало top_coins с запросом {query}')
            kwargs["data"] = ControllerGlobalStats.__get_data_top_coins(kwargs["bot"].coinmarketcap_token, int(query))
        except:
            kwargs["bot"].logger.info(f'Начало top_coins с запросом {20}')
            kwargs["data"] = ControllerGlobalStats.__get_data_top_coins(kwargs["bot"].coinmarketcap_token)
        ViewGlobalStats.top_coins(message, **kwargs)

    @staticmethod
    def menu_global_stats(call, **kwargs):
        kwargs["bot"].logger.info(f'Начало global_stats')
        kwargs["data"] = ControllerGlobalStats.__get_data_for_global_stats(kwargs["bot"].coinmarketcap_token)
        ViewGlobalStats.menu_global_stats(call, **kwargs)

    @staticmethod
    def menu_top_coins(call, **kwargs):
        kwargs["bot"].logger.info(f'Начало top_coins с запросом {20}')
        kwargs["data"] = ControllerGlobalStats.__get_data_top_coins(kwargs["bot"].coinmarketcap_token)
        ViewGlobalStats.menu_top_coins(call, **kwargs)

    @staticmethod
    def __get_data_for_global_stats(coinmarketcap_token):
        # Создаём запрос к CoinMarketCap
        url = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest"
        headers = {
            "X-CMC_PRO_API_KEY": coinmarketcap_token
        }
        # Отправляем запрос и получаем данные
        coinmarketcap_response = requests.get(url, headers=headers)
        if coinmarketcap_response.status_code not in [200, 300]:
            return {"error": "Не удалось получить данные из запроса"}

        coinmarketcap_response_data = coinmarketcap_response.json()

        # Создаём запрос к Alternative
        url = "https://api.alternative.me/fng/?limit=0"
        alternative_response = requests.get(url)
        alternative_response_data = json.loads(alternative_response.text)

        aggregated_data = {
            "btc_dominance": coinmarketcap_response_data["data"]["btc_dominance"],
            "eth_dominance": coinmarketcap_response_data["data"]["eth_dominance"],
            "usd_total_market_cap": coinmarketcap_response_data["data"]["quote"]["USD"]["total_market_cap"],
            "usd_total_volume_24h_percentage_change": coinmarketcap_response_data["data"]["quote"]["USD"]["total_volume_24h_yesterday_percentage_change"],
            "usd_total_volume_24h_reported": coinmarketcap_response_data["data"]["quote"]["USD"]["total_volume_24h_reported"],
            "usd_stablecoin_volume_24h_reported": coinmarketcap_response_data["data"]["quote"]["USD"]["stablecoin_volume_24h_reported"],
            "usd_altcoin_volume_24h_reported": coinmarketcap_response_data["data"]["quote"]["USD"]["altcoin_volume_24h_reported"],
            "today_fear_and_greed_index": int(alternative_response_data["data"][0]["value"])
        }

        return aggregated_data

    @staticmethod
    def __get_data_top_coins(coinmarketcap_token, amount_of_coins=20):
        if amount_of_coins > 50:
            amount_of_coins = 50

        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        params = {
            "limit": amount_of_coins,
        }
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": coinmarketcap_token,
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code not in [200, 300]:
            return {"error": "Не удалось получить данные из запроса"}

        response_data = response.json()

        top_coins = response_data["data"]
        for coin in top_coins:
            del coin["tags"]

        aggregated_data = {
            "top_coins": top_coins,
            "amount_of_coins": amount_of_coins
        }

        return aggregated_data
