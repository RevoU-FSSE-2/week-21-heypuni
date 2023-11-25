from flask import Flask
from routes.auth import auth_bp
from routes.tweet import tweet_bp
from routes.following import following_bp
from routes.user import user_bp
from configs import db, bcrypt

app = Flask(__name__)

# Konfigurasi database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(tweet_bp)
app.register_blueprint(following_bp)
app.register_blueprint(user_bp, url_prefix="/user")


if __name__ == "__main__":
    with app.app_context():
        bcrypt.init_app(app)
        db.init_app(app)
        db.drop_all()
        db.create_all()
    app.run(debug=True)
