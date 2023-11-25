from marshmallow import Schema, fields


class UserFollowing(Schema):
    user_id = fields.Integer(required=True)
