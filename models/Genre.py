from mysql_manage import db
from datetime import datetime

class Genre(db.Model):
    __tablename__ = "genre"

    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(500))
    genre_url_keyword = db.Column(db.String(500))
    source_site = db.Column(db.String(500))

    def __init__(self, genre_name, genre_url_keyword, source_site):
        self.genre_name = genre_name
        self.genre_url_keyword = genre_url_keyword
        self.source_site = source_site

    # Return a nice JSON response
    def serialize(self):
        return {
            'genre_id': self.genre_id,
            'genre_url_keyword': self.genre_url_keyword,
            'genre_name': self.genre_name,
            'source_site': self.source_site,
        }
