class ViewMenu:
    @staticmethod
    def get_menu(message, **kwargs):
        kwargs["bot"].send_message(message.chat.id, "Меню", reply_markup=kwargs["bot"].markup_of_tg_menu())