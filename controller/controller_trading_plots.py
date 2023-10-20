from view.view_trading_plots import ViewTradingPlots
import requests
import re
import numpy as np


class ControllerTradingPlots:
    @staticmethod
    def ohlc(message, **kwargs):
        try:
            pattern = r"\s(?P<currency>\w+)(\s(?P<value>\d+|max))?"
            match = re.search(pattern, message.text)

            query = match.groupdict()

            if "currency" in query.keys() and "value" in query.keys():
                kwargs["bot"].logger.info(f'Начало построения ohlc по крипте: {query["currency"]} с кол-вом дней: {query["value"]}')
                kwargs["data"] = ControllerTradingPlots.__get_data_from_request_ohlc(
                    kwargs["bot"].coingecko_token,
                    query["currency"],
                    query["value"],
                    kwargs["bot"].coins_data
                )
            elif "currency" in query.keys():
                kwargs["bot"].logger.info(f'Начало построения ohlc по крипте: {query["currency"]} с кол-вом дней: {30}')
                kwargs["data"] = ControllerTradingPlots.__get_data_from_request_ohlc(
                    kwargs["bot"].coingecko_token,
                    query["currency"],
                    30,
                    kwargs["bot"].coins_data
                )
            else:
                raise Exception

        except:
            kwargs["bot"].logger.info(f'Ошибка при построении ohlc')
            kwargs["data"] = {"error": "Неправильно переданы аргументы для расчётов"}

        ViewTradingPlots.ohlc(message, **kwargs)

    @staticmethod
    def market_chart(message, **kwargs):
        try:
            pattern = r"\s(?P<currency>\w+)(\s(?P<value>\d+|max))?"
            match = re.search(pattern, message.text)

            query = match.groupdict()

            if "currency" in query.keys() and "value" in query.keys():
                kwargs["bot"].logger.info(f'Начало построения market_chart по крипте: {query["currency"]} с кол-вом дней: {query["value"]}')
                kwargs["data"] = ControllerTradingPlots.__get_data_from_request_market_chart(
                    kwargs["bot"].coingecko_token,
                    query["currency"],
                    query["value"],
                    kwargs["bot"].coins_data
                )
            elif "currency" in query.keys():
                kwargs["bot"].logger.info(f'Начало построения market_chart по крипте: {query["currency"]} с кол-вом дней: {30}')
                kwargs["data"] = ControllerTradingPlots.__get_data_from_request_market_chart(
                    kwargs["bot"].coingecko_token,
                    query["currency"],
                    30,
                    kwargs["bot"].coins_data
                )
            else:
                raise Exception
        except:
            kwargs["bot"].logger.info(f'Ошибка при построении market_chart')
            kwargs["data"] = {"error": "Неправильно переданы аргументы для расчётов"}

        ViewTradingPlots.market_chart(message, **kwargs)

    @staticmethod
    def __get_data_from_request_ohlc(coingecko_token, coin_id, days, coins_data):
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc?vs_currency=usd&days={days}"
        headers = {
            "Content-Type": "application/json",
            "X-CoinGecko-Api-Key": coingecko_token,
        }
        response = requests.get(url, headers=headers)
        if response.status_code not in [200, 300]:
            return {"error": "Не удалось получить данные из запроса"}

        response_data = response.json()
        response_data = np.array(response_data).T.tolist()

        aggregated_data = {
            "time": response_data[0],
            "open": response_data[1],
            "high": response_data[2],
            "low": response_data[3],
            "close": response_data[4],
            "coin_id": coin_id,
            "iso": coins_data.iso[coin_id],
            "days": days
        }

        return aggregated_data


    @staticmethod
    def __get_data_from_request_market_chart(coingecko_token, coin_id, days, coins_data):
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}"
        headers = {
            "Content-Type": "application/json",
            "X-CoinGecko-Api-Key": coingecko_token,
        }
        response = requests.get(url, headers=headers)
        if response.status_code not in [200, 300]:
            return {"error": "Не удалось получить данные из запроса"}

        response_data = response.json()

        prices = np.array(response_data["prices"]).T.tolist()
        market_caps = np.array(response_data["market_caps"]).T.tolist()
        total_volumes = np.array(response_data["total_volumes"]).T.tolist()

        aggregated_data = {
            "time": prices[0],
            "prices": prices[1],
            "market_caps": market_caps[1],
            "total_volumes": total_volumes[1],
            "coin_id": coin_id,
            "iso": coins_data.iso[coin_id],
            "days": days
        }

        return aggregated_data
