from dbm import dumb
from decimal import Clamped
from marshmallow import Schema,fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    username = fields.Str()
    email = fields.Str()
    join_date = fields.Date(dump_only=True)


class NotesSchema(Schema):
    id = fields.Int(dump_only=True)
    data = fields.Str()
    date = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)

 