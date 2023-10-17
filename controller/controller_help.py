from view.view_help import ViewHelp
import re


class ControllerHelp:
    @staticmethod
    def help(message, **kwargs):
        query = re.findall(r"\D+ [\/]?([\w]+)", message.text)

        if query == []:
            ViewHelp.help(message, **kwargs)
        elif query[0] == "global_stats":
            ViewHelp.help_global_stats(message, **kwargs)
        elif query[0] == "top_coins":
            ViewHelp.help_top_coins(message, **kwargs)
        elif query[0] == "crypto_stats":
            ViewHelp.help_crypto_stats(message, **kwargs)
        elif query[0] == "stacking_info":
            ViewHelp.help_stacking_info(message, **kwargs)
        elif query[0] == "fear_and_greed_data":
            ViewHelp.help_fear_and_greed_data(message, **kwargs)
        elif query[0] == "ohlc":
            ViewHelp.help_ohlc(message, **kwargs)
        elif query[0] == "market_chart":
            ViewHelp.help_market_chart(message, **kwargs)

        elif query[0] == "create_asset_portfolio":
            ViewHelp.help_create_asset_portfolio(message, **kwargs)
        elif query[0] == "change_asset":
            ViewHelp.help_change_asset(message, **kwargs)
        elif query[0] == "delete_asset":
            ViewHelp.help_delete_asset(message, **kwargs)
        elif query[0] == "get_assets":
            ViewHelp.help_get_assets(message, **kwargs)
        elif query[0] == "visualise_asset_portfolio":
            ViewHelp.help_visualise_asset_portfolio(message, **kwargs)
        elif query[0] == "assets_portfolio_changes":
            ViewHelp.help_assets_portfolio_changes(message, **kwargs)
        else:
            ViewHelp.no_command(message, **kwargs)

