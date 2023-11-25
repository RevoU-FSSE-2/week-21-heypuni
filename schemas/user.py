from marshmallow import fields, Schema


class UserRegistration(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    bio = fields.String(required=True)
