import telebot
import logging
import sys
from apscheduler.schedulers.background import BackgroundScheduler

from controller.controller_help import ControllerHelp
from controller.controller_global_stats import ControllerGlobalStats
from controller.controller_crypto_stats import ControllerCryptoStats
from controller.controller_stacking import ControllerStacking
from controller.controller_fear_and_greed_data import ControllerFeatAndGreedData
from controller.controller_trading_plots import ControllerTradingPlots
from controller.controller_protfolio import ControllerPortfolio

from model.db import DB
from model.coingecko_coins_data import CoingeckoCoinsData


class TGBot(telebot.TeleBot):
    def __init__(self, **kwargs):
        super().__init__(kwargs["bot_config"].tg_token)
        self.__set_logger()
        self.__register_handler()

        # Установка токенов
        self.tg_token = kwargs["bot_config"].tg_token
        self.coinmarketcap_token = kwargs["bot_config"].coinmarketcap_token
        self.coingecko_token = kwargs["bot_config"].coingecko_token
        self.stakingrewards_token = kwargs["bot_config"].stakingrewards_token
        self.cryptorank_token = kwargs["bot_config"].cryptorank_token

        self.db = DB(path_to_db_file=kwargs["db_config"].path_to_db_file)
        self.coins_data = CoingeckoCoinsData(self.coingecko_token)

        # Создаём расписание, чтобы обновлять информацию о крипте через определённое кол-во часов
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.__update_coins_data, trigger="interval", hours=6)
        self.scheduler.start()

    # Настройка логгера
    def __set_logger(self):
        #self.logger = telebot.logger
        self.logger = logging.getLogger('logger')
        formatter = logging.Formatter('[%(asctime)s] %(thread)d %(levelname)s - %(message)s',
                                      '%m-%d %H:%M:%S')
        ch = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(ch)
        self.logger.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)

    def __register_handler(self):
        # Общие функции работы с агрегаторами
        self.register_message_handler(ControllerHelp.help, commands=['help'], pass_bot=True)
        self.register_message_handler(ControllerGlobalStats.global_stats, commands=['global_stats'], pass_bot=True)
        self.register_message_handler(ControllerGlobalStats.top_coins, commands=['top_coins'], pass_bot=True)
        self.register_message_handler(ControllerCryptoStats.crypto_stats, commands=['crypto_stats'], pass_bot=True)
        self.register_message_handler(ControllerStacking.stacking_info, commands=['stacking_info'], pass_bot=True)
        self.register_message_handler(ControllerFeatAndGreedData.fear_and_greed_data, commands=['fear_and_greed_data'], pass_bot=True)
        self.register_message_handler(ControllerTradingPlots.ohlc, commands=['ohlc'], pass_bot=True)
        self.register_message_handler(ControllerTradingPlots.market_chart, commands=['market_chart'], pass_bot=True)

        # Функции портфеля активов
        self.register_message_handler(ControllerPortfolio.create_users_portfolio, commands=['create_asset_portfolio'], pass_bot=True)
        self.register_message_handler(ControllerPortfolio.change_asset_in_portfolio, commands=['change_asset'], pass_bot=True)
        self.register_message_handler(ControllerPortfolio.delete_asset_from_portfolio, commands=['delete_asset'], pass_bot=True)
        self.register_message_handler(ControllerPortfolio.get_assets_from_portfolio, commands=['get_assets'], pass_bot=True)
        self.register_message_handler(ControllerPortfolio.visualise_asset_portfolio, commands=['visualise_asset_portfolio'], pass_bot=True)
        self.register_message_handler(ControllerPortfolio.assets_portfolio_changes, commands=['assets_portfolio_changes'], pass_bot=True)

    def __update_coins_data(self):
        self.coins_data = CoingeckoCoinsData(self.coingecko_token)
