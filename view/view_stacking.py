class ViewStacking:
    @staticmethod
    def stacking_info(message, **kwargs):
        if "error" in kwargs["data"].keys():
            kwargs["bot"].send_message(
                message.chat.id,
                kwargs["data"]["error"]
            )
        else:
            print_data = (
                f'Информация о стейкинге {kwargs["data"]["name"]}:\n\n'
                f'* Средний APR на сегодня {round(kwargs["data"]["apr"], 2)} % \n'
                f'* Провайдеры и их APR на сегодня:\n'
            )
            for provider in kwargs["data"]["providers"]:
                print_data += f'   * {provider["slug"]}: {round(provider["rewardOptions"][0]["metrics"][0]["defaultValue"], 2)} % \n'

            kwargs["bot"].send_message(
                message.chat.id,
                print_data
            )
