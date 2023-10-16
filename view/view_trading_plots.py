import plotly.graph_objs as go
from plotly.subplots import make_subplots
from kaleido.scopes.plotly import PlotlyScope

import numpy as np
import pandas as pd


scope = PlotlyScope()


class ViewTradingPlots:
    @staticmethod
    def ohlc(message, **kwargs):
        if "error" in kwargs["data"].keys():
            kwargs["bot"].send_message(
                message.chat.id,
                kwargs["data"]["error"]
            )
        else:
            kwargs["bot"].send_message(
                message.chat.id,
                f'OHLC для {kwargs["data"]["coin_id"]} за последние {kwargs["data"]["days"]} дней'
            )
            kwargs["bot"].send_photo(
                message.chat.id,
                ViewTradingPlots.__create_ohlc_plot(kwargs["data"])
            )

    @staticmethod
    def market_chart(message, **kwargs):
        if "error" in kwargs["data"].keys():
            kwargs["bot"].send_message(
                message.chat.id,
                kwargs["data"]["error"]
            )
        else:
            kwargs["bot"].send_message(
                message.chat.id,
                f'График для {kwargs["data"]["coin_id"]} за последние {kwargs["data"]["days"]} дней'
            )
            kwargs["bot"].send_photo(
                message.chat.id,
                ViewTradingPlots.__create_market_chart_plot(kwargs["data"])
            )

    @staticmethod
    def __create_ohlc_plot(data):
        global scope

        COUNT_OF_ROWS = len(data["time"])
        DAYS = data["days"]
        ISO = data["iso"].upper()
        DATA_COUNT_MULTIPLIER = COUNT_OF_ROWS / 40
        WHISKERWIDTH = 1 if 0.5 * DATA_COUNT_MULTIPLIER > 1 else 0.5 * DATA_COUNT_MULTIPLIER
        BARGAP = 1 if 0.25 * DATA_COUNT_MULTIPLIER > 1 else 0.25 * np.sqrt(DATA_COUNT_MULTIPLIER)

        data = pd.DataFrame({
            "date": data["time"],
            "open": data["open"],
            "high": data["high"],
            "low": data["low"],
            "close": data["close"]
        })
        data["volume"] = np.nan
        data["date"] = pd.to_datetime(data["date"], unit="ms")
        data.index = pd.DatetimeIndex(data['date'])

        print(data.shape)

        # Создаём график на котором будут отобображаться свечи и циклюрующие USDT
        fig = make_subplots(
            rows=2, cols=1,
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
            row_heights=[0.9, 0.2],
            vertical_spacing=0.
        )

        # Построение визуализаций

        # В фигуру вставляем диаграмму Японских свечей
        fig.add_trace(
            go.Candlestick(
                # Данные по которым будут строится свечи
                x=data.iloc[:COUNT_OF_ROWS]['date'],
                open=data.iloc[:COUNT_OF_ROWS]['open'],
                high=data.iloc[:COUNT_OF_ROWS]['high'],
                low=data.iloc[:COUNT_OF_ROWS]['low'],
                close=data.iloc[:COUNT_OF_ROWS]['close'],
                # Ширина линий
                line={"width": 2.5 / DATA_COUNT_MULTIPLIER},
                # Усы на концах максимумов и минимумов
                whiskerwidth=WHISKERWIDTH,
                # Установка цвета
                increasing={"fillcolor": "#0ED181", "line": {"color": "#0ED181"}},
                decreasing={"fillcolor": "#F6465D", "line": {"color": "#F6465D"}}
            ),
            # Эта визуализация не является вторичной
            secondary_y=False,
            # Указываем месторасположение
            row=1, col=1
        )

        # Добавляем индикатор изменения цены закрытий
        if data.iloc[:COUNT_OF_ROWS]['close'].iloc[0] <= data.iloc[:COUNT_OF_ROWS]['close'].iloc[-1]:
            fig.add_trace(
                go.Indicator(
                    mode="number+delta",
                    value=data.iloc[:COUNT_OF_ROWS]['close'].iloc[-1],
                    number={"font": {"size": 13}},
                    delta={
                        'reference': data.iloc[:COUNT_OF_ROWS]['close'].iloc[0],
                        'relative': True,
                        "font": {"size": 13},
                        "valueformat": ".3%",
                        # "suffix": "%",
                        # "prefix": "%"
                    },
                    domain={'x': [0.75, 1], 'y': [0.9, 1]}
                )
            )
        else:
            fig.add_trace(
                go.Indicator(
                    mode="number+delta",
                    value=data.iloc[:COUNT_OF_ROWS]['close'].iloc[-1],
                    number={"font": {"size": 13}},
                    delta={
                        'reference': data.iloc[:COUNT_OF_ROWS]['close'].iloc[0],
                        'relative': True,
                        "font": {"size": 13},
                        "valueformat": ".3%",
                        # "suffix": "%",
                        # "prefix": "%"
                    },
                    domain={'x': [0.75, 1], 'y': [0.2, 0.3]}
                )
            )

        # Цвета для Box (красный - понижение, зелёный - понижение)
        colors = []
        for i in range(COUNT_OF_ROWS):
            if data.iloc[i]['open'] < data.iloc[i]['close']:
                colors += ["#0ED181"]
            else:
                colors += ["#F6465D"]

        # В фигуру вставляем объём циркулирующих USDT
        if DATA_COUNT_MULTIPLIER < 10:
            fig.add_trace(
                go.Bar(
                    # Данные по которым будет строится визуализация
                    x=data.iloc[:COUNT_OF_ROWS]['date'],
                    y=data.iloc[:COUNT_OF_ROWS]['volume'],
                    # Цвет столбцов
                    marker_color=colors,
                    # Настройка линии для столбцов
                    marker_line={"width": 2, "color": colors},
                    opacity=0.6
                ),
                # Эта визуализация не является вторичной
                secondary_y=False,
                # Указываем месторасположение
                row=2, col=1
            )
        else:
            fig.add_trace(
                go.Scatter(
                    # Данные по которым будет строится визуализация
                    x=data.iloc[:COUNT_OF_ROWS]['date'],
                    y=data.iloc[:COUNT_OF_ROWS]['volume'],
                    # Настраиваем маркеры
                    mode='markers',
                    marker={"color": colors, "size": 3},
                    opacity=0.6
                ),
                # Эта визуализация не является вторичной
                secondary_y=False,
                # Указываем месторасположение
                row=2, col=1
            )

        # Добавляем аннотацию для максимального значения
        fig.add_annotation(
            # Данные для отображение максимума
            x=data.iloc[:COUNT_OF_ROWS].loc[data.iloc[:COUNT_OF_ROWS]["high"].idxmax()]["date"],
            y=data.iloc[:COUNT_OF_ROWS]["high"].max(),
            # Максимальная цена за единицу валюты
            text="Max " + str(data.iloc[:COUNT_OF_ROWS]["high"].max()),
            # Отключаем построение стрелочки
            showarrow=False,
            # Кстанавливаем шрифт
            font={"size": 11, "color": "#ffffff"},
            # Текст будем выводить на 20 ед. выше
            yshift=20
        )

        # Добавляем аннотацию для минимального значения
        fig.add_annotation(
            # Данные для отображение минимума
            x=data.iloc[:COUNT_OF_ROWS].loc[data.iloc[:COUNT_OF_ROWS]["low"].idxmin()]["date"],
            y=data.iloc[:COUNT_OF_ROWS]["low"].min(),
            # Минимальная цена за единицу валюты
            text="Min " + str(data.iloc[:COUNT_OF_ROWS]["low"].min()),
            # Отключаем построение стрелочки
            showarrow=False,
            # Кстанавливаем шрифт
            font={"size": 11, "color": "#ffffff"},
            # Текст будем выводить на 20 ед. ниже
            yshift=-20
        )

        # Настройка визуализации
        # Отключаем отображение значений осей Y для вторичных визуализаций
        fig.layout.yaxis2.update(showticklabels=False, showgrid=False, zeroline=False)
        fig.layout.yaxis4.update(showticklabels=False, showgrid=False, zeroline=False)
        # Устанавливаем отступы для визуализации
        fig.layout.margin = {"l": 10, "r": 10, "t": 50, "b": 10}
        # Устанавливаем оглавление визуализации
        fig.layout.title.update(text=f"{ISO}/USD   ({DAYS} days)", xanchor="center", yanchor="top", x=0.2,
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
        fig.layout.yaxis1.update(tickmode="array",
                                 tickvals=
                                     np.linspace(data.iloc[:COUNT_OF_ROWS]['low'].min(),
                                                 data.iloc[:COUNT_OF_ROWS]['high'].max(),
                                                 14),
                                 tickformat='.5f')

        # Отключаем ось X для визуализации Японских свечей
        fig.layout.xaxis.update(showticklabels=False, zeroline=False)

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
                   "linewidth": 0, "gridwidth": 1.5, 'visible': True, 'showticklabels': False,
                   "range": [data.iloc[:COUNT_OF_ROWS]["date"].min(), data.iloc[:COUNT_OF_ROWS]["date"].max()]},
            # Стиль оси X для столбчатой диаграммы
            xaxis2={"ticks": "outside", "tickson": "labels", "ticklen": 10, "linecolor": "#464C56",
                    "gridcolor": "#282D37",
                    "range": [data.iloc[:COUNT_OF_ROWS]["date"].min(), data.iloc[:COUNT_OF_ROWS]["date"].max()],
                    "linewidth": 0, "gridwidth": 1.5},
            # Стиль оси Y для Японских свечей
            yaxis={"showgrid": True, "linecolor": "#464C56", "gridcolor": "#282D37",
                   "linewidth": 2, "gridwidth": 1.5},
            # Стиль оси Y для столбчатой диаграммы
            yaxis3={"zeroline": False, "linecolor": "#464C56", "gridcolor": "#282D37",
                    "linewidth": 2, "gridwidth": 1.5}
        )

        fig.update_layout(
            autosize=False,
            width=800,
            height=600,
        )

        # Сохранение картинки в бинарном формате
        fig_str = scope.transform(fig, format="png", scale=3)

        return fig_str

    @staticmethod
    def __create_market_chart_plot(data):
        global scope

        COUNT_OF_ROWS = len(data["time"])
        DAYS = data["days"]
        ISO = data["iso"].upper()
        DATA_COUNT_MULTIPLIER = COUNT_OF_ROWS / 40
        BARGAP = 1 if 0.25 * DATA_COUNT_MULTIPLIER > 1 else 0.25 * np.sqrt(DATA_COUNT_MULTIPLIER)

        data = pd.DataFrame({
            "date": data["time"],
            "prices": data["prices"],
            "market_caps": data["market_caps"],
            "volume": data["total_volumes"]
        })
        data["date"] = pd.to_datetime(data["date"], unit="ms")
        data.index = pd.DatetimeIndex(data['date'])
        data[["prices_above", "prices_below"]] = np.nan

        print(data.shape)

        mask_above = data.iloc[0]['prices'] <= data.iloc[:COUNT_OF_ROWS]['prices']
        data.iloc[:COUNT_OF_ROWS].loc[:, "prices_above"] = np.where(mask_above, data.iloc[:COUNT_OF_ROWS]['prices'],
                                                                    np.nan)
        data.iloc[:COUNT_OF_ROWS].loc[:, "prices_below"] = np.where(mask_above, np.nan,
                                                                    data.iloc[:COUNT_OF_ROWS]['prices'])

        # Создаём график на котором будут отобображаться свечи и циклюрующие USDT
        fig = make_subplots(
            rows=2, cols=1,
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
            row_heights=[0.9, 0.2],
            vertical_spacing=0.
        )

        # Построение визуализаций

        # В фигуру вставляем диаграмму Японских свечей
        fig.add_trace(
            go.Scatter(
                # Данные по которым будут строится свечи
                x=data.iloc[:COUNT_OF_ROWS]['date'],
                y=data.iloc[:COUNT_OF_ROWS]['prices'],
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
                x=data.iloc[:COUNT_OF_ROWS]['date'],
                y=data.iloc[:COUNT_OF_ROWS]['prices_above'],
                line={"width": 2.5},
                mode='markers',
                marker_color='#0ED181'
            ),
            # Эта визуализация не является вторичной
            secondary_y=False,
            # Указываем месторасположение
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
                # Данные по которым будут строится свечи
                x=data.iloc[:COUNT_OF_ROWS]['date'],
                y=data.iloc[:COUNT_OF_ROWS]['prices_below'],
                line={"width": 2.5},
                mode='markers',
                marker_color='#F6465D'
            ),
            # Эта визуализация не является вторичной
            secondary_y=False,
            # Указываем месторасположение
            row=1, col=1
        )

        fig.add_hline(y=data.iloc[0]['prices'], line_width=2.5, line_dash="dash",
                      annotation=dict(font_size=12, bgcolor="#FFFFFF"),
                      annotation_font_color="#687180",
                      annotation_text=f"<b>{round(data.iloc[0]['prices'], 5)}</b>",
                      annotation_position="left",
                      line_color="purple")

        # Цвета для Box (красный - понижение, зелёный - понижение)
        colors = []
        for i in range(COUNT_OF_ROWS):
            colors += ["#405969"]
            #if data.iloc[i]['open'] < data.iloc[i]['close']:
            #    colors += ["#0ED181"]
            #else:
            #    colors += ["#F6465D"]

        # В фигуру вставляем объём циркулирующих USDT
        if DATA_COUNT_MULTIPLIER < 10:
            fig.add_trace(
                go.Bar(
                    # Данные по которым будет строится визуализация
                    x=data.iloc[:COUNT_OF_ROWS]['date'],
                    y=data.iloc[:COUNT_OF_ROWS]['volume'],
                    # Цвет столбцов
                    marker_color=colors,
                    # Настройка линии для столбцов
                    marker_line={"width": 2, "color": colors},
                    opacity=0.6
                ),
                # Эта визуализация не является вторичной
                secondary_y=False,
                # Указываем месторасположение
                row=2, col=1
            )
        else:
            fig.add_trace(
                go.Scatter(
                    # Данные по которым будет строится визуализация
                    x=data.iloc[:COUNT_OF_ROWS]['date'],
                    y=data.iloc[:COUNT_OF_ROWS]['volume'],
                    # Настраиваем маркеры
                    mode='markers',
                    marker={"color": colors, "size": 3},
                    opacity=0.6
                ),
                # Эта визуализация не является вторичной
                secondary_y=False,
                # Указываем месторасположение
                row=2, col=1
            )

        # Настройка визуализации
        # Отключаем отображение значений осей Y для вторичных визуализаций
        fig.layout.yaxis2.update(showticklabels=False, showgrid=False, zeroline=False)
        fig.layout.yaxis4.update(showticklabels=False, showgrid=False, zeroline=False)
        # Устанавливаем отступы для визуализации
        fig.layout.margin = {"l": 10, "r": 10, "t": 50, "b": 10}
        # Устанавливаем оглавление визуализации
        fig.layout.title.update(text=f"{ISO}/USD   ({DAYS} days)", xanchor="center", yanchor="top", x=0.2,
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
        fig.layout.yaxis1.update(tickmode="array",
                                 tickvals=
                                     np.linspace(data['prices'].min(),
                                                 data['prices'].max(),
                                                 14),
                                 tickformat='.5f')

        # Отключаем ось X для визуализации Японских свечей
        fig.layout.xaxis.update(showticklabels=False, zeroline=False)

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
                   "linewidth": 0, "gridwidth": 1.5, 'visible': True, 'showticklabels': False,
                   "range": [data.iloc[:COUNT_OF_ROWS]["date"].min(), data.iloc[:COUNT_OF_ROWS]["date"].max()]},
            # Стиль оси X для столбчатой диаграммы
            xaxis2={"ticks": "outside", "tickson": "labels", "ticklen": 10, "linecolor": "#464C56",
                    "gridcolor": "#282D37",
                    "range": [data.iloc[:COUNT_OF_ROWS]["date"].min(), data.iloc[:COUNT_OF_ROWS]["date"].max()],
                    "linewidth": 0, "gridwidth": 1.5},
            # Стиль оси Y для Японских свечей
            yaxis={"showgrid": True, "linecolor": "#464C56", "gridcolor": "#282D37",
                   "linewidth": 2, "gridwidth": 1.5},
            # Стиль оси Y для столбчатой диаграммы
            yaxis3={"zeroline": False, "linecolor": "#464C56", "gridcolor": "#282D37",
                    "linewidth": 2, "gridwidth": 1.5}
        )

        fig.update_layout(
            autosize=False,
            width=800,
            height=600,
        )

        # Сохранение картинки в бинарном формате
        fig_str = scope.transform(fig, format="png", scale=3)

        return fig_str
