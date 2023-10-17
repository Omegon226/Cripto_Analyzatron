import plotly.graph_objs as go
from plotly.subplots import make_subplots
from kaleido.scopes.plotly import PlotlyScope

import numpy as np
import pandas as pd


scope = PlotlyScope()


class ViewFeatAndGreedData:
    @staticmethod
    def fear_and_greed_data(message, **kwargs):
        if "error" in kwargs["data"].keys():
            kwargs["bot"].send_message(
                message.chat.id,
                kwargs["data"]["error"]
            )
        else:
            kwargs["bot"].send_message(
                message.chat.id,
                f'Данные по индексу страха и жадности:\n\n'
                f'* Текущий индекс страха и жадности: {kwargs["data"]["data"][0]["value"]}'
            )
            kwargs["bot"].send_photo(
                message.chat.id,
                ViewFeatAndGreedData.__create_fear_and_greed_timeseries(kwargs["data"])
            )

    @staticmethod
    def menu_fear_and_greed_data(call, **kwargs):
        kwargs["bot"].answer_callback_query(call.id, "Данные за 90 дней по F&G индексу выведены")
        if "error" in kwargs["data"].keys():
            kwargs["bot"].send_message(
                call.from_user.id,
                kwargs["data"]["error"]
            )
        else:
            kwargs["bot"].send_message(
                call.from_user.id,
                f'Данные по индексу страха и жадности:\n\n'
                f'* Текущий индекс страха и жадности: {kwargs["data"]["data"][0]["value"]}'
            )
            kwargs["bot"].send_photo(
                call.from_user.id,
                ViewFeatAndGreedData.__create_fear_and_greed_timeseries(kwargs["data"])
            )

    @staticmethod
    def __create_fear_and_greed_timeseries(data):
        global scope

        COUNT_OF_ROWS = data["period_days"]
        DATA_COUNT_MULTIPLIER = COUNT_OF_ROWS / 40
        BARGAP = 1 if 0.25 * DATA_COUNT_MULTIPLIER > 1 else 0.25 * np.sqrt(DATA_COUNT_MULTIPLIER)

        del data["data"][0]["time_until_update"]

        data = pd.DataFrame(data["data"])
        data["value"] = data['value'].astype('int')
        data["timestamp"] = pd.to_datetime(data["timestamp"], unit="s")

        # Создаём график на котором будут отобображаться свечи и циклюрующие USDT
        fig = make_subplots()

        # Построение визуализаций

        # В фигуру вставляем диаграмму Японских свечей
        fig.add_trace(
            go.Scatter(
                # Данные по которым будут строится свечи
                x=data.iloc[:COUNT_OF_ROWS]['timestamp'],
                y=data.iloc[:COUNT_OF_ROWS]['value'],
                line={"width": 1.5},
                mode='lines',
                marker_color='#687180'
            ),
            # Эта визуализация не является вторичной
            secondary_y=False,
            # Указываем месторасположение
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
                # Данные по которым будут строится свечи
                x=data.iloc[:COUNT_OF_ROWS]['timestamp'].where(data.iloc[:COUNT_OF_ROWS]['value'] <= 20),
                y=data.iloc[:COUNT_OF_ROWS]['value'].where(data.iloc[:COUNT_OF_ROWS]['value'] <= 20),
                line={"width": 2.5},
                mode='markers',
                marker_color='#EA3943'
            ),
            # Эта визуализация не является вторичной
            secondary_y=False,
            # Указываем месторасположение
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
                # Данные по которым будут строится свечи
                x=data.iloc[:COUNT_OF_ROWS]['timestamp'].where(
                    (20 < data.iloc[:COUNT_OF_ROWS]['value']) & (data.iloc[:COUNT_OF_ROWS]['value'] <= 40)),
                y=data.iloc[:COUNT_OF_ROWS]['value'].where(
                    (20 < data.iloc[:COUNT_OF_ROWS]['value']) & (data.iloc[:COUNT_OF_ROWS]['value'] <= 40)),
                line={"width": 2.5},
                mode='markers',
                marker_color='#EA8C00'
            ),
            # Эта визуализация не является вторичной
            secondary_y=False,
            # Указываем месторасположение
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
                # Данные по которым будут строится свечи
                x=data.iloc[:COUNT_OF_ROWS]['timestamp'].where(
                    (40 < data.iloc[:COUNT_OF_ROWS]['value']) & (data.iloc[:COUNT_OF_ROWS]['value'] <= 60)),
                y=data.iloc[:COUNT_OF_ROWS]['value'].where(
                    (40 < data.iloc[:COUNT_OF_ROWS]['value']) & (data.iloc[:COUNT_OF_ROWS]['value'] <= 60)),
                line={"width": 2.5},
                mode='markers',
                marker_color='#F3D42F'
            ),
            # Эта визуализация не является вторичной
            secondary_y=False,
            # Указываем месторасположение
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
                # Данные по которым будут строится свечи
                x=data.iloc[:COUNT_OF_ROWS]['timestamp'].where(
                    (60 < data.iloc[:COUNT_OF_ROWS]['value']) & (data.iloc[:COUNT_OF_ROWS]['value'] <= 80)),
                y=data.iloc[:COUNT_OF_ROWS]['value'].where(
                    (60 < data.iloc[:COUNT_OF_ROWS]['value']) & (data.iloc[:COUNT_OF_ROWS]['value'] <= 80)),
                line={"width": 2.5},
                mode='markers',
                marker_color='#93D900'
            ),
            # Эта визуализация не является вторичной
            secondary_y=False,
            # Указываем месторасположение
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
                # Данные по которым будут строится свечи
                x=data.iloc[:COUNT_OF_ROWS]['timestamp'].where(
                    (80 < data.iloc[:COUNT_OF_ROWS]['value']) & (data.iloc[:COUNT_OF_ROWS]['value'] <= 100)),
                y=data.iloc[:COUNT_OF_ROWS]['value'].where(
                    (80 < data.iloc[:COUNT_OF_ROWS]['value']) & (data.iloc[:COUNT_OF_ROWS]['value'] <= 100)),
                line={"width": 2.5},
                mode='markers',
                marker_color='#16C784'
            ),
            # Эта визуализация не является вторичной
            secondary_y=False,
            # Указываем месторасположение
            row=1, col=1
        )

        # Настройка визуализации
        # Устанавливаем отступы для визуализации
        fig.layout.margin = {"l": 10, "r": 10, "t": 50, "b": 10}
        # Устанавливаем оглавление визуализации
        fig.layout.title.update(text=f"Fear & Greed index ({COUNT_OF_ROWS} days)", xanchor="center", yanchor="top", x=0.25,
                                font={'color': 'white', "family": "Arial", "size": 24})
        # Устанавливаем размер отступа между столбцами
        fig.layout.bargap = BARGAP
        # Отключение слайдера
        fig.layout.xaxis.rangeslider = {'visible': False}
        # Отключение легенды
        fig.layout.showlegend = False
        # Настройка оcей Y для всех визуализаций в фигуре
        fig.update_yaxes(ticks="outside", tickson="labels", ticklen=10)
        # Настройка тиков для оси X для свечей
        # fig.layout.yaxis1.update(tickmode="array",
        #                          tickvals=np.round(
        #                              np.linspace(data.iloc[:COUNT_OF_ROWS]['low'].min(),
        #                                          data.iloc[:COUNT_OF_ROWS]['high'].max(),
        #                                          14), 0))

        # Настройка цветов для фигуры
        fig.update_layout(
            # Цвет фона графика
            plot_bgcolor="#161A1E",
            # Цвет фона области графика
            paper_bgcolor="#161A1E",
            # Цвет шрифта
            font={"color": "#687180"},
            # Стиль оси X для Японских свечей
            xaxis={"showgrid": True, "linecolor": "#464C56", "gridcolor": "#282D37",
                   "linewidth": 0, "gridwidth": 1.5, 'visible': True, 'showticklabels': True},

            # Стиль оси Y для Японских свечей
            yaxis={"showgrid": True, "linecolor": "#464C56", "gridcolor": "#282D37",
                   "linewidth": 2, "gridwidth": 1.5},
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
