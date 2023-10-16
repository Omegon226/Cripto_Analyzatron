from view.view_portfolio import ViewPortfolio
import requests
import re
import humanize
import numpy as np
import pandas as pd
from copy import deepcopy
import time


class ControllerPortfolio:
    @staticmethod
    def create_users_portfolio(message, **kwargs):
        kwargs["bot"].logger.info(f'Начало create_users_portfolio')
        kwargs["bot"].db.create_or_wipe_portfolio(message.from_user.id)
        ViewPortfolio.create_users_portfolio(message, **kwargs)

    @staticmethod
    def change_asset_in_portfolio(message, **kwargs):
        try:
            query = re.findall(r"\D+ ([\w\-\_]+) ([\d,.]+)", message.text)
            kwargs["bot"].logger.info(f'Начало change_asset_in_portfolio с запросом {query}')
            assets_info = {}

            for data in query:
                asset = data[0]
                amount = float(data[1].replace(",", "."))

                if asset in kwargs["bot"].coins_data.coins:
                    kwargs["bot"].db.add_or_change_asset(message.from_user.id, asset, amount)
                    assets_info[asset] = "Success"
                else:
                    assets_info[asset] = "Failure"

            kwargs["data"] = {"result_of_additing": assets_info}
            ViewPortfolio.change_asset_in_portfolio(message, **kwargs)
        except:
            kwargs["data"] = {"error": "Не получилось добавить или изменить актив"}
            ViewPortfolio.change_asset_in_portfolio(message, **kwargs)

    @staticmethod
    def delete_asset_from_portfolio(message, **kwargs):
        try:
            query = re.findall(r"\/[a-zA-Z_]+ ([\w]+)", message.text)
            kwargs["bot"].logger.info(f'Начало delete_asset_from_portfolio с запросом {query}')
            for asset in query:
                kwargs["bot"].db.delete_asset(message.from_user.id, asset)

            ViewPortfolio.delete_asset_from_portfolio(message, **kwargs)
        except:
            kwargs["data"] = {"error": "Не получилось удалить актив"}
            ViewPortfolio.delete_asset_from_portfolio(message, **kwargs)

    @staticmethod
    def get_assets_from_portfolio(message, **kwargs):
        kwargs["bot"].logger.info(f'Начало get_assets_from_portfolio')
        kwargs["data"] = kwargs["bot"].db.get_portfolio(message.from_user.id)
        ViewPortfolio.get_assets_from_portfolio(message, **kwargs)

    @staticmethod
    def visualise_asset_portfolio(message, **kwargs):
        kwargs["bot"].logger.info(f'Начало visualise_asset_portfolio')
        portfolio = kwargs["bot"].db.get_portfolio(message.from_user.id)
        data = {"name": [], "price": [], "amount": []}

        for coin in portfolio:
            data["name"] += [kwargs["bot"].coins_data.iso[coin].upper()]
            data["price"] += [ControllerPortfolio.__get_price_of_coin(coin, kwargs["bot"].coingecko_token)]
            data["amount"] += [portfolio[coin]]

        portfolio = pd.DataFrame(data)
        portfolio["sum"] = portfolio["price"] * portfolio["amount"]
        portfolio_price = portfolio["sum"].sum()

        kwargs["data"] = {"portfolio": portfolio, "portfolio_price": portfolio_price}

        ViewPortfolio.visualise_asset_portfolio(message, **kwargs)

    @staticmethod
    def assets_portfolio_changes(message, **kwargs):
        kwargs["bot"].logger.info(f'Начало assets_portfolio_changes')
        prices = None

        portfolio = kwargs["bot"].db.get_portfolio(message.from_user.id)

        for idx, coin in enumerate(portfolio):
            print(coin)
            price = ControllerPortfolio.__get_price_of_coin_timeseries(coin, kwargs["bot"].coingecko_token)

            if price is None:
                continue

            if idx == 0:
                prices = price
            else:
                prices[coin] = price[coin]

        sum_for_portfolio = deepcopy(prices)
        for coin in sum_for_portfolio.columns:
            sum_for_portfolio.loc[:, coin] *= portfolio[coin]

        summary_table = pd.DataFrame({
            "name": [list(portfolio.keys())[0] for i in range(sum_for_portfolio.shape[0])],
            "date": sum_for_portfolio.index,
            "price": prices[list(portfolio.keys())[0]],
            "sum": sum_for_portfolio[list(portfolio.keys())[0]]
        })

        for coin in list(portfolio.keys())[1:]:
            try:
                new_df = pd.DataFrame({
                    "name": [coin for _ in range(sum_for_portfolio.shape[0])],
                    "date": sum_for_portfolio.index,
                    "price": prices[coin],
                    "sum": sum_for_portfolio[coin]
                })

                summary_table = pd.concat([summary_table, new_df])
            except:
                pass

        kwargs["data"] = {"summary_table": summary_table}

        ViewPortfolio.assets_portfolio_changes(message, **kwargs)

    @staticmethod
    def __get_price_of_coin(crypto_id, coingecko_token):
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
        headers = {
            "x_cg_demo_api_key": coingecko_token
        }
        response = requests.get(url, headers=headers)
        if response not in [200, 300]:
            return {"error": "Не удалось получить данные из запроса"}

        response_data = response.json()
        price = response_data[crypto_id]["usd"]
        return price

    @staticmethod
    def __get_price_of_coin_timeseries(crypto_id, coingecko_token):
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
            params = {
                "vs_currency": "usd",
                "days": "30"
            }
            headers = {
                "Content-Type": "application/json",
                "X-CoinGecko-Api-Key": coingecko_token,
            }
            response = requests.get(url, params=params, headers=headers)
            if response not in [200, 300]:
                return {"error": "Не удалось получить данные из запроса"}

            response_data = response.json()
            price = np.array(response_data["prices"])
            price = pd.DataFrame({
                "date": price[:, 0],
                crypto_id: price[:, 1]
            })
            price["date"] = pd.to_datetime(price["date"], unit="ms")
            price = price.resample('D', on='date').mean()
            return price
        except:
            return None
