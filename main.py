from model.tg_bot import TGBot
from config import BotConfig, DbConfig

if __name__ == "__main__":
    bot = TGBot(bot_config=BotConfig, db_config=DbConfig)

    bot.logger.info("Пошёл процесс")
    bot.polling(none_stop=True)
