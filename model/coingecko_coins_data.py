import requests
import json


class CoingeckoCoinsData:
    def __init__(self, coingecko_token, use_api=False):

        if use_api:
            try:
                self.coins, self.iso = self.__get_all_coins_id(coingecko_token)
                self.__save_data()
            except:
                self.coins, self.iso = self.__load_data()
        else:
            self.coins, self.iso = self.__load_data()

    def __get_all_coins_id(self, coingecko_token):
        url = "https://api.coingecko.com/api/v3/coins/list"
        headers = {
            "Content-Type": "application/json",
            "X-CoinGecko-Api-Key": coingecko_token,
        }
        response = requests.get(url, headers=headers)
        if response.status_code not in [200, 300]:
            raise Exception

        response_data = response.json()
        coins = []
        iso = {}
        for coin in response_data:
            coins += [coin["id"]]
            iso[coin["id"]] = coin["symbol"]

        return coins, iso

    def __save_data(self):
        with open("resources/coins_from_coingecko_api.json", "w") as file:
            json.dump({"coins": self.coins, "iso": self.iso}, file)

    def __load_data(self):
        with open("resources/coins_from_coingecko_api.json", "r") as file:
            data = json.load(file)

            coins = data["coins"]
            iso = data["iso"]

        return coins, iso
