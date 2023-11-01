from . import db

class Actor( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    surname = db.Column(db.Text)
    bdate = db.Column(db.Date)
    country = db.Column(db.Text, db.ForeignKey('country.name', ondelete='cascade'))
    actors1 = db.relationship('Actor_in_film', backref='actor1', lazy='dynamic')

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, default=0)
    year = db.Column(db.Integer)
    description = db.Column(db.Text)
    films1 = db.relationship('Actor_in_film', backref='film1', lazy='dynamic')
    films2 = db.relationship('Genre_in_film', backref='film2', lazy='dynamic')
    films3 = db.relationship('Film_director', backref='film3', lazy='dynamic')
    films4 = db.relationship('Review', backref='film4', lazy='dynamic')
    films5 = db.relationship('User_films', backref='film5', lazy='dynamic')

class Genre(db.Model):
    name = db.Column(db.Text, primary_key=True)
    genres = db.relationship('Genre_in_film', backref='genre1', lazy='dynamic')

class User(db.Model):
    login = db.Column(db.Text, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    users1 = db.relationship('Review', backref='user1', lazy='dynamic')
    users2 = db.relationship('User_films', backref='user2', lazy='dynamic')

class Country(db.Model):
    name = db.Column(db.Text, primary_key=True)
    countries1 = db.relationship('Film_by_country', backref='country1', lazy='dynamic')
    countries2 = db.relationship('Actor', backref='country2', lazy='dynamic')
    countries3 = db.relationship('Director', backref='country3', lazy='dynamic')

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id', ondelete='cascade'))
    rating = db.Column(db.Float)
    review_header = db.Column(db.Text)
    review_text = db.Column(db.Text)
    user = db.Column(db.Text, db.ForeignKey('user.login', ondelete='cascade'))

class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    surname = db.Column(db.Text)
    bdate = db.Column(db.Date)
    country = db.Column(db.Text, db.ForeignKey('country.name', ondelete='cascade'))
    director1 = db.relationship('Film_director', backref='director1', lazy='dynamic')

class Film_director(db.Model):
    dir_id = db.Column(db.Integer, db.ForeignKey('director.id', ondelete='cascade'), primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id', ondelete='cascade'), primary_key=True)

class Actor_in_film(db.Model):
    act_id = db.Column(db.Integer, db.ForeignKey('actor.id', ondelete='cascade'), primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id', ondelete='cascade'), primary_key=True)

class Genre_in_film(db.Model):
    film_id = db.Column(db.Integer, db.ForeignKey('film.id', ondelete='cascade'), primary_key=True)
    genre_id = db.Column(db.Text, db.ForeignKey('genre.name', ondelete='cascade'), primary_key=True)

class Film_by_country(db.Model):
    film_id = db.Column(db.Integer, db.ForeignKey('film.id', ondelete='cascade'), primary_key=True)
    country_id = db.Column(db.Text, db.ForeignKey('country.name', ondelete='cascade'), primary_key=True)

class User_films(db.Model):
    film_id = db.Column(db.Integer, db.ForeignKey('film.id', ondelete='cascade'), primary_key=True)
    user = db.Column(db.Text, db.ForeignKey('user.login', ondelete='cascade'), primary_key=True)


