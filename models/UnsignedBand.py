from mysql_manage import db
from datetime import datetime

class UnsignedBand(db.Model):
    __tablename__ = "unsignedband"

    p_id = db.Column(db.Integer, primary_key=True)
    ranking = db.Column(db.Integer)
    last_ranking = db.Column(db.Integer)
    image_link = db.Column(db.Text)
    name = db.Column(db.String(500))
    song_artist_name = db.Column(db.String(500))
    artist_page_link = db.Column(db.Text)
    genre_id = db.Column(db.Integer)
    rank_date = db.Column(db.String(100))
    source_site = db.Column(db.String(100))

    def __init__(self, ranking, last_ranking, image_link, name, song_artist_name,
                 artist_page_link, genre_id, rank_date, source_site):
        
        self.ranking = ranking
        self.last_ranking = last_ranking
        self.image_link = image_link
        self.name = name
        self.song_artist_name = song_artist_name
        self.artist_page_link = artist_page_link
        self.genre_id = genre_id
        self.rank_date = rank_date
        self.source_site = source_site

    # Return a nice JSON response
    def serialize(self):
        return {
            'p_id': self.p_id,
            'ranking': self.ranking,
            'last_ranking': self.last_ranking,
            'image_link': self.image_link,
            'name': self.name,
            'song_artist_name': self.song_artist_name,
            'artist_page_link': self.artist_page_link,
            'genre_id': self.genre_id,
            'rank_date': self.rank_date,
            'source_site': self.source_site,
        }
