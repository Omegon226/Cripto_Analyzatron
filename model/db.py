from tinydb import TinyDB, Query


class DB(TinyDB):
    def __init__(self, **kwargs):
        super().__init__(kwargs["path_to_db_file"])
        self.query = Query()

    def create_or_wipe_portfolio(self, user_id):
        try:
            if len(self.search(self.query.user_id == user_id)) > 0:
                self.update({"user_id": user_id, "portfolio": {}}, self.query.user_id == user_id)
            else:
                self.insert({"user_id": user_id, "portfolio": {}})
        except Exception as error:
            raise error

    def add_or_change_asset(self, user_id, asset, amount):
        try:
            portfolio = self.get_portfolio(user_id)
            portfolio[asset] = amount
            self.update({"portfolio": portfolio}, self.query.user_id == user_id)
        except Exception as error:
            raise error

    def delete_asset(self, user_id, asset):
        try:
            portfolio = self.get_portfolio(user_id)
            del portfolio[asset]
            self.update({"portfolio": portfolio}, self.query.user_id == user_id)
        except Exception as error:
            raise error

    def get_portfolio(self, user_id):
        try:
            return self.search(self.query.user_id == user_id)[0]["portfolio"]
        except Exception as error:
            raise error

    def get_all_data(self):
        try:
            return self.all()
        except Exception as error:
            raise error
