from flask import Flask
from app.auth.apis import auth_bp
from app.follow.apis import follow_bp
from app.tweet.apis import tweet_bp
from app.user.apis import user_bp
from db import db, db_init
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(follow_bp, url_prefix='/follow')
app.register_blueprint(tweet_bp, url_prefix='/tweet')
app.register_blueprint(user_bp, url_prefix='/user-profile')

# with app.app_context():
#     db_init()