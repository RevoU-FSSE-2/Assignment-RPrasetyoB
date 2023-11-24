from datetime import datetime
from db import db


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    published_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tweet_text = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'<Tweet {self.id}>'