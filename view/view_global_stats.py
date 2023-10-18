import plotly.graph_objs as go
from kaleido.scopes.plotly import PlotlyScope

import humanize


scope = PlotlyScope()


class ViewGlobalStats:
    @staticmethod
    def global_stats(message, **kwargs):
        if "error" in kwargs["data"].keys():
            kwargs["bot"].send_message(
                message.chat.id,
                kwargs["data"]["error"]
            )
        else:
            kwargs["bot"].send_message(
                message.chat.id,
                f'Глобальная статистика рынка:\n\n'
                f'* Доминация BTC: {round(kwargs["data"]["btc_dominance"], 2)} %\n'
                f'* Доминация ETH: {round(kwargs["data"]["eth_dominance"], 2)} %\n'
                f'* Капитализация рынка: {humanize.intword(kwargs["data"]["usd_total_market_cap"], "%0.2f")} $\n'
                f'* Изменение капитализации рынка за 24 часа: {round(kwargs["data"]["usd_total_volume_24h_percentage_change"], 2)} %\n'
                f'* Рыночное цирк-ее кол-во долларов: {humanize.intword(kwargs["data"]["usd_total_volume_24h_reported"], "%0.2f")} $\n'
                f'* Рыночное цирк-ее кол-во стейблкоинов: {humanize.intword(kwargs["data"]["usd_stablecoin_volume_24h_reported"], "%0.2f")} $\n'
                f'* Циркулирующее кол-во долларов в альткойнах: {humanize.intword(kwargs["data"]["usd_altcoin_volume_24h_reported"], "%0.2f")} $'
            )
            kwargs["bot"].send_photo(
                message.chat.id,
                ViewGlobalStats.__create_fear_and_greed_plot(kwargs["data"]["today_fear_and_greed_index"])
            )

    @staticmethod
    def top_coins(message, **kwargs):
        if "error" in kwargs["data"].keys():
            kwargs["bot"].send_message(
                message.chat.id,
                kwargs["data"]["error"]
            )
        else:
            print_data = f'Топ {kwargs["data"]["amount_of_coins"]} монет:\n\n'
            for idx, coin in enumerate(kwargs["data"]["top_coins"]):
                print_data += f'{idx+1}) {coin["symbol"]} ({coin["slug"]}) Цена: {round(coin["quote"]["USD"]["price"], 8):f} $\n'

                if len(print_data) > 3500:
                    kwargs["bot"].send_message(
                        message.chat.id,
                        print_data
                    )
                    print_data = ""
            if len(print_data) > 0:
                kwargs["bot"].send_message(
                    message.chat.id,
                    print_data
                )

    @staticmethod
    def menu_global_stats(call, **kwargs):
        kwargs["bot"].answer_callback_query(call.id, "Глобальные данные о крипторынке получены")
        if "error" in kwargs["data"].keys():
            kwargs["bot"].send_message(
                call.from_user.id,
                kwargs["data"]["error"]
            )
        else:
            kwargs["bot"].send_message(
                call.from_user.id,
                f'Глобальная статистика рынка:\n\n'
                f'* Доминация BTC: {round(kwargs["data"]["btc_dominance"], 2)} %\n'
                f'* Доминация ETH: {round(kwargs["data"]["eth_dominance"], 2)} %\n'
                f'* Капитализация рынка: {humanize.intword(kwargs["data"]["usd_total_market_cap"], "%0.2f")} $\n'
                f'* Изменение капитализации рынка за 24 часа: {round(kwargs["data"]["usd_total_volume_24h_percentage_change"], 2)} %\n'
                f'* Рыночное цирк-ее кол-во долларов: {humanize.intword(kwargs["data"]["usd_total_volume_24h_reported"], "%0.2f")} $\n'
                f'* Рыночное цирк-ее кол-во стейблкоинов: {humanize.intword(kwargs["data"]["usd_stablecoin_volume_24h_reported"], "%0.2f")} $\n'
                f'* Циркулирующее кол-во долларов в альткойнах: {humanize.intword(kwargs["data"]["usd_altcoin_volume_24h_reported"], "%0.2f")} $'
            )
            kwargs["bot"].send_photo(
                call.from_user.id,
                ViewGlobalStats.__create_fear_and_greed_plot(kwargs["data"]["today_fear_and_greed_index"])
            )

    @staticmethod
    def menu_top_coins(call, **kwargs):
        kwargs["bot"].answer_callback_query(call.id, "Топ 20 криптовалют получено")
        if "error" in kwargs["data"].keys():
            kwargs["bot"].send_message(
                call.from_user.id,
                kwargs["data"]["error"]
            )
        else:
            print_data = (
                f'Топ {kwargs["data"]["amount_of_coins"]} монет:\n\n'
            )
            for idx, coin in enumerate(kwargs["data"]["top_coins"]):
                print_data += f'{idx+1}) {coin["symbol"]} ({coin["slug"]}) Цена: {round(coin["quote"]["USD"]["price"], 8):f} $\n'

            kwargs["bot"].send_message(
                call.from_user.id,
                print_data
            )


    @staticmethod
    def __create_fear_and_greed_plot(fear_and_greed_index):
        global scope

        FEAR_AND_GREED_INDEX = fear_and_greed_index
        if FEAR_AND_GREED_INDEX <= 20:
            COLOR_FOR_BAR = "#EA3943"
        elif 20 < FEAR_AND_GREED_INDEX <= 40:
            COLOR_FOR_BAR = "#EA8C00"
        elif 40 < FEAR_AND_GREED_INDEX <= 60:
            COLOR_FOR_BAR = "#F3D42F"
        elif 60 < FEAR_AND_GREED_INDEX <= 80:
            COLOR_FOR_BAR = "#93D900"
        elif 80 < FEAR_AND_GREED_INDEX <= 100:
            COLOR_FOR_BAR = "#16C784"

        fig = go.Figure(go.Indicator(
            domain={'x': [0, 1], 'y': [0, 1]},
            value=FEAR_AND_GREED_INDEX,
            mode="gauge+number",
            gauge={'axis': {'range': [None, 100]},
                   'bar': {'color': COLOR_FOR_BAR},
                   'steps': [
                       {'range': [0, 100], 'color': "#687180"}],
                   }))

        # Устанавливаем оглавление визуализации
        fig.layout.title.update(text="Fear & Greed Index", xanchor="center", yanchor="top", x=0.5,
                                font={'color': 'white', "family": "Arial", "size": 32})

        # Устанавливаем отступы для визуализации
        fig.layout.margin = {"l": 100, "r": 100, "t": 95, "b": 20}

        fig.update_layout(
            # Цвет фона графика
            plot_bgcolor="#161A1E",
            # Цвет фона области графика
            paper_bgcolor="#161A1E",
            # Цвет шрифта
            font={"color": "#FFFFFF", "size": 18},
        )

        # Устанавливаем фиксированный размер визуализации
        fig.update_layout(
            autosize=False,
            width=800,
            height=600,
        )

        # Сохранение картинки в бинарном формате
        fig_str = scope.transform(fig, format="png", scale=3)

        return fig_str
