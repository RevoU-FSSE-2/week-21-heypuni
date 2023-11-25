from marshmallow import fields, Schema


class TweetSchema(Schema):
    tweet = fields.String(required=True)
