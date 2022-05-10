from datetime import datetime

from gino import Gino

db = Gino()


class AbsModel(db.Model):
    """ Abstract class for updating data using model """

    def __init__(self, *args, **kwargs):
        self.__updates = dict()
        super().__init__(*args, **kwargs)

    def __setattr__(self, key, value):
        if key in self._column_name_map:
            self.__updates.update({key: value})
        return super().__setattr__(key, value)

    @property
    def upd(self):
        return self.__updates

    async def apply_updates(self):
        res = await self.update(**self.__updates).apply()
        self.__updates.clear()
        return res

    async def create(self, *args, **kwargs):
        self.__updates.clear()
        return await super().create(*args, **kwargs)


class Users(AbsModel):
    """
    Model with user information.
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String)

    __tablename__ = "users"


class Brands(AbsModel):
    """
    Model with brand information.
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, index=True)

    __tablename__ = "brands"


class DiscountCodes(AbsModel):
    """
    Model with discount codes information.
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand_id = db.Column(db.Integer, db.ForeignKey(Brands.id, ondelete='CASCADE'), index=True)
    code = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'), index=True, nullable=True)

    __tablename__ = "discount_codes"
