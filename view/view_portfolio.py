import plotly
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from kaleido.scopes.plotly import PlotlyScope

import numpy as np
import pandas as pd

import humanize

scope = PlotlyScope()


class ViewPortfolio:
    @staticmethod
    def create_users_portfolio(message, **kwargs):
        if "error" in kwargs["data"].keys():
            kwargs["bot"].send_message(
                message.chat.id,
                kwargs["data"]["error"]
            )
        else:
            kwargs["bot"].send_message(
                message.chat.id,
                "Ваш портфель был создан! Теперь вы можете добавлять туда свои активы"
            )

    @staticmethod
    def change_asset_in_portfolio(message, **kwargs):
        if "error" in kwargs["data"].keys():
            kwargs["bot"].send_message(
                message.chat.id,
                kwargs["data"]["error"]
            )
        else:
            failure_assets = []

            for asset in kwargs["data"]["result_of_additing"].keys():
                if kwargs["data"]["result_of_additing"][asset] == "Failure":
                    failure_assets += [asset]

            if len(failure_assets) == 0:
                print_data = "Все активы были добавлены успешно!"
            elif len(failure_assets) > 0:
                print_data = "Активы были добавлены, но некоторые не получилось добавить. Попробуйте поменять их название\n"
                print_data += f"Не добавлены следующие активы: {' ,'.join(failure_assets)}"
            elif len(failure_assets) == len(kwargs["data"]["result_of_additing"]):
                print_data = "Активы не были добавлены"
            else:
                print_data = "ABOBA"

            kwargs["bot"].send_message(
                message.chat.id,
                print_data
            )

    @staticmethod
    def delete_asset_from_portfolio(message, **kwargs):
        if "error" in kwargs["data"].keys():
            kwargs["bot"].send_message(
                message.chat.id,
                kwargs["data"]["error"]
            )
        else:
            kwargs["bot"].send_message(
                message.chat.id,
                "Актив/ы были удалены из вашего портфеля"
            )

    @staticmethod
    def get_assets_from_portfolio(message, **kwargs):
        if "error" in kwargs["data"].keys():
            kwargs["bot"].send_message(
                message.chat.id,
                kwargs["data"]["error"]
            )
        else:
            print_data = "Ваш портфель:\n\n"

            for coin in kwargs["data"].keys():
                print_data += f'* {coin}: {kwargs["data"][coin]}\n'

            kwargs["bot"].send_message(
                message.chat.id,
                print_data
            )

    @staticmethod
    def visualise_asset_portfolio(message, **kwargs):
        if "error" in kwargs["data"].keys():
            kwargs["bot"].send_message(
                message.chat.id,
                kwargs["data"]["error"]
            )
        else:
            kwargs["bot"].send_photo(
                message.chat.id,
                ViewPortfolio.__create_asset_portfolio_pie(kwargs["data"])
            )

    @staticmethod
    def assets_portfolio_changes(message, **kwargs):
        if "error" in kwargs["data"].keys():
            kwargs["bot"].send_message(
                message.chat.id,
                kwargs["data"]["error"]
            )
        else:
            kwargs["bot"].send_photo(
                message.chat.id,
                ViewPortfolio.__create_portfolio_changes_bar(kwargs["data"])
            )

    @staticmethod
    def __create_asset_portfolio_pie(data):
        global scope

        portfolio = data["portfolio"]
        portfolio_price = data["portfolio_price"]

        # Создаём график на котором будут отобображаться свечи и циклюрующие USDT
        fig = make_subplots()

        fig.add_trace(
            go.Pie(
                labels=portfolio["name"],
                values=portfolio["sum"]
            )
        )

        fig.update_traces(
            # Добавляем отверстие по середине Pie
            hole=.6,
            # hoverinfo="label+percent+name+value"
            # Цветовая палитра для Pie
            marker={"colors": px.colors.qualitative.Vivid},
            # Информация которая будет выводится на участках Pie
            textinfo='label+percent'
        )

        fig.update_layout(
            # Цвет фона графика
            plot_bgcolor="#161A1E",
            # Цвет фона области графика
            paper_bgcolor="#161A1E",
            # Цвет шрифта
            font={"color": "#687180"},
            # Отключаем показ легенды
            showlegend=False,
            # Добавляем суммарный размер портфеля
            annotations=[
                {
                    "text": humanize.intword(portfolio_price, "%0.2f") + '<br>USD',
                    "x": 0.5,
                    "y": 0.5,
                    "font_size": 20,
                    "showarrow": False
                }
            ]
        )

        # Изменяем ширфт, названия визуализации и информации в этой визуализации
        fig.update_layout(font={"color": "#FFFFFF"})
        fig.update_traces(textfont_color="#FFFFFF", textfont_size=13)

        # Устанавливаем оглавление визуализации
        fig.layout.title.update(text="Your actives", xanchor="center", yanchor="top", x=0.5,
                                font={'color': 'white', "family": "Arial", "size": 32})

        # Устанавливаем отступы для визуализации
        fig.layout.margin = {"l": 10, "r": 10, "t": 95, "b": 20}

        # Устанавливаем фиксированный размер визуализации
        fig.update_layout(
            autosize=False,
            width=800,
            height=600,
        )

        # Сохранение картинки в бинарном формате
        fig_str = scope.transform(fig, format="png", scale=3)

        return fig_str

    @staticmethod
    def __create_portfolio_changes_bar(data):
        global scope

        summary_table = data["summary_table"]

        # Создание визуализации
        fig = px.bar(
            summary_table,
            x="date",
            y="sum",
            color="name",
            text="sum",
            color_discrete_sequence=px.colors.qualitative.Vivid
        )

        # Устанавливаем информацию, которая будет выводится в столбчатой диаграмме
        fig.update_traces(
            # Информация, положение, цвет и размер текста, который будет в bar
            # texttemplate='%{text:0.3s}<br>USDT',
            texttemplate='%{text:0.3s}',
            textposition='inside',
            textfont_color="#FFFFFF",
            textfont_size=14,
            # Настройка угла вывода информации внутри bar
            textangle=0,
            # Отключаем белую линию, отделяющую элементы bar
            marker_line_width=0
        )

        # Настройка цветов визуализации
        fig.update_layout(
            # Цвет фона графика
            plot_bgcolor="#161A1E",
            # Цвет фона области графика
            paper_bgcolor="#161A1E",
            # Цвет шрифта
            font={"color": "#687180"},
        )

        # Установка обязательной вывода легенды
        fig.update_layout(showlegend=True)

        # Устанавливаем оглавление визуализации
        fig.layout.title.update(
            text="Your actives price change",
            xanchor="center",
            yanchor="top",
            x=0.5,
            font={
                'color': 'white',
                "family": "Arial",
                "size": 32
            }
        )

        # Устанавливаем отступы для визуализации
        fig.layout.margin = {"l": 10, "r": 30, "t": 95, "b": 20}

        # Отключаем вывод названия осей и легенды
        fig.layout.yaxis.title = None
        fig.layout.xaxis.title = None
        fig.layout.legend.title.text = None

        # Настройка цветов для фигуры
        fig.update_layout(
            # Стиль оси X для Японских свечей
            xaxis={"showgrid": True, "linecolor": "#464C56", "gridcolor": "#282D37",
                   "linewidth": 0, "gridwidth": 1.5, 'visible': True},
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
