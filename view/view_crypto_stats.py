import humanize
from datetime import datetime


class ViewCryptoStats:
    @staticmethod
    def crypto_stats(message, **kwargs):
        kwargs["bot"].send_message(
            message.chat.id,
            f'Информация о {kwargs["data"]["symbol"]}:\n\n'
            f'* Дата создания: {datetime.strptime(kwargs["data"]["date_added"], "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%d")}\n'
            f'* Название: {kwargs["data"]["name"]}\n'
            f'* Алгоритмы: {", ".join(kwargs["data"]["algorithms"])}\n'
            f'* Циркулирующее предложение: {kwargs["data"]["circulating_supply"]}\n'
            f'* Максимальное предложение: {kwargs["data"]["max_supply"]}\n'
            f'* Капитализация: {humanize.intword(kwargs["data"]["usd_fully_diluted_market_cap"], "%0.2f")} $\n'
            f'* Цена: {kwargs["data"]["usd_price"]} $\n'
            f'* Кол-во торговых пар: {kwargs["data"]["num_market_pairs"]}\n'
            f'* Изменение цены за 1 час: {round(kwargs["data"]["usd_percent_change_1h"], 2)} %\n'
            f'* Изменение цены за 24 часа: {round(kwargs["data"]["usd_percent_change_24h"], 2)} %\n'
            f'* Изменение цены за 7 дней: {round(kwargs["data"]["usd_percent_change_7d"], 2)} %\n'
            f'* Изменение цены за 30 дней: {round(kwargs["data"]["usd_percent_change_30d"], 2)} %\n'
            f'* Изменение цены за 60 дней: {round(kwargs["data"]["usd_percent_change_60d"], 2)} %\n'
            f'* Изменение цены за 90 дней: {round(kwargs["data"]["usd_percent_change_90d"], 2)} %\n'
        )
