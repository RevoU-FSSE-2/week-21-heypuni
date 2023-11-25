from config import db


class Tweet(db.Model):
    __tablename__ = "tweets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    published_at = db.Column(db.DateTime, nullable=False)
    tweet = db.Column(db.String(150), nullable=False)
