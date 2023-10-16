from view.view_crypto_stats import ViewCryptoStats
import requests
import pandas as pd
import re


class ControllerCryptoStats:
    @staticmethod
    def crypto_stats(message, **kwargs):
        query = re.findall(r"\D+ ([\w]+)", message.text)[0]

        kwargs["data"] = ControllerCryptoStats.__get_data_from_request(kwargs["bot"].coinmarketcap_token, kwargs["bot"].coingecko_token, query)
        ViewCryptoStats.crypto_stats(message, **kwargs)

    @staticmethod
    def __get_data_from_request(coinmarketcap_token, coingecko_token, coin_slug):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/info"
        parameters = {
            "slug": coin_slug
        }
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": coinmarketcap_token,
        }
        coinmarketcap_response_1 = requests.get(url, params=parameters, headers=headers)
        coinmarketcap_response_1_data = coinmarketcap_response_1.json()
        coin_id = list(coinmarketcap_response_1_data["data"].keys())[0]

        coinmarketcap_response_1_data = pd.DataFrame({
            "tag-groups": coinmarketcap_response_1_data["data"][coin_id]["tag-groups"],
            "tag-names": coinmarketcap_response_1_data["data"][coin_id]["tag-names"]
        })
        coinmarketcap_response_1_data = coinmarketcap_response_1_data[
            (coinmarketcap_response_1_data["tag-groups"] == "ALGORITHM") |
            (coinmarketcap_response_1_data["tag-groups"] == "OTHERS")
        ]["tag-names"].values.tolist()

        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        parameters = {
            "slug": coin_slug,
            "convert": "USD"
        }
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": coinmarketcap_token,
        }
        coinmarketcap_response_2 = requests.get(url, params=parameters, headers=headers)
        coinmarketcap_response_2_data = coinmarketcap_response_2.json()["data"][coin_id]

        aggregated_data = {
            "date_added": coinmarketcap_response_2_data['date_added'],
            "symbol": coinmarketcap_response_2_data['symbol'],
            "name": coinmarketcap_response_2_data['name'],
            "algorithms": coinmarketcap_response_1_data,
            "circulating_supply": coinmarketcap_response_2_data['circulating_supply'],
            "max_supply": coinmarketcap_response_2_data['max_supply'],
            "usd_fully_diluted_market_cap": coinmarketcap_response_2_data['quote']['USD']['fully_diluted_market_cap'],
            "usd_price": coinmarketcap_response_2_data['quote']['USD']['price'],
            "num_market_pairs": coinmarketcap_response_2_data['num_market_pairs'],
            "usd_percent_change_1h": coinmarketcap_response_2_data['quote']['USD']['percent_change_1h'],
            "usd_percent_change_24h": coinmarketcap_response_2_data['quote']['USD']['percent_change_24h'],
            "usd_percent_change_7d": coinmarketcap_response_2_data['quote']['USD']['percent_change_7d'],
            "usd_percent_change_30d": coinmarketcap_response_2_data['quote']['USD']['percent_change_30d'],
            "usd_percent_change_60d": coinmarketcap_response_2_data['quote']['USD']['percent_change_60d'],
            "usd_percent_change_90d": coinmarketcap_response_2_data['quote']['USD']['percent_change_90d']
        }

        return aggregated_data
