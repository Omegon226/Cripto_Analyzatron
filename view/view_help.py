class ViewHelp:
    @staticmethod
    def help(message, **kwargs):
        kwargs["bot"].send_message(
            message.chat.id,
            "Существующие команды:\n\n"
            "* /global_stats - отображает глобальную статистику рынка\n"
            "* /ohlc {ISO крипты} - визуализация японских свечей\n"
            "* /market_chart {ISO крипты} {период} - визуализация тренда \n"
            "* /crypto_stats {ISO крипты} - вывод основной статистики криптовалюты\n"
            "* /stacking_info {ISO крипты} - информация о стейкинге криптовалюты\n"
            "* /fear_and_greed_data - отображает изменение индекса страха и жадности за последнее время\n"
            "* /create_asset_portfolio - создание/обнуление портфеля активов\n"
            "* /change_asset {ISO крипты} {кол-во} - задать или изменить данные об активе в портфеле\n"
            "* /delet_asset {ISO крипты} - удалить актив из портфеля\n"
            "* /visualise_asset_portfolio - визуализация активов\n"
            "* /assets_portfolio_changes - изменение цены портфеля \n"
        )
