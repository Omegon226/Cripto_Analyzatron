import os
import yaml
from yaml.loader import SafeLoader


class BotConfig:
    with open('resources/tokens.yaml', "r") as file:
        tokens = yaml.load(file, Loader=SafeLoader)

    tg_token = tokens["tg_token"]
    coinmarketcap_token = tokens["coinmarketcap_token"]
    coingecko_token = tokens["coingecko_token"]
    stakingrewards_token = tokens["stakingrewards_token"]
    cryptorank_token = tokens["cryptorank_token"]


class DbConfig:
    path_to_db_file = "resources/portfolios_db.json"
