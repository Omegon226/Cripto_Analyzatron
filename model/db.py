from tinydb import TinyDB, Query


class DB(TinyDB):
    def __init__(self, **kwargs):
        super().__init__(kwargs["path_to_db_file"])
        self.query = Query()

    def create_or_wipe_portfolio(self, user_id):
        try:
            if len(self.search(self.query.user_id == user_id)) > 0:
                self.update({"user_id": user_id, "portfolio": {}}, self.query.user_id == user_id)
                return {"success": "Портфель был очищен"}
            else:
                self.insert({"user_id": user_id, "portfolio": {}})
                return {"success": "Портфель был создан! Теперь вы можете добавлять туда свои актив"}
        except Exception as error:
            raise error

    def add_or_change_asset(self, user_id, asset, amount):
        try:
            portfolio = self.get_portfolio(user_id)["result"]
            portfolio[asset] = amount
            self.update({"portfolio": portfolio}, self.query.user_id == user_id)
            return {"success": f"Актив {asset} был добавлен или изменён"}
        except Exception as error:
            raise error

    def delete_asset(self, user_id, asset):
        try:
            portfolio = self.get_portfolio(user_id)["result"]
            del portfolio[asset]
            self.update({"portfolio": portfolio}, self.query.user_id == user_id)
            return {"success": f"Актив {asset} был из портфеля"}
        except Exception as error:
            raise error

    def get_portfolio(self, user_id):
        try:
            return {
                "result": self.search(self.query.user_id == user_id)[0]["portfolio"],
                "success": f"Ваше портфель был успешно получен"
            }
        except Exception as error:
            raise error

    def get_all_data(self):
        try:
            return {
                "result": self.all(),
                "success": f"Данные всех портфелей были успешно получены"
            }
        except Exception as error:
            raise error
