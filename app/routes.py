from flask import render_template, flash, redirect, url_for, request, g, session
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import *
from app import app, db
from sqlalchemy import exc
from app.__init__ import adm_pwd

@app.before_request
def load_logged_in_user():
    login = session.get('login')
    if login is None:
        g.user = None
    else:
        g.user = User.query.filter_by(login = login).first()

@app.route('/')
@app.route('/index/<messages>')
@app.route('/index')
def index(messages=None):
    if messages:
        flash(messages)
    return render_template('index.html', title='Главная страница')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        error = None
        user = User.query.filter_by(login = login).first()
        if user is None:
            error = f"Пользователь с логином \"{login}\" не найден ."
        elif not check_password_hash(user.password, password):
            error = f"Пароль пользователя \"{login}\" неверен."
        if error is None:
            session.clear()
            session['login'] = user.login
        else:
            flash(error)
        return redirect(url_for('index'))
    else:
        return render_template('login.html', title='Вход')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form['password']
        error = None
        if not check_password_hash(adm_pwd, password):
            error = f"Пароль администратора некорректен."
        if error is None:
            user = User.query.filter_by(login = g.user.login).first()
            user.is_admin = True
            db.session.commit()
            error = f"Пользователь \"{user.login}\" становится администратором."
            return redirect(url_for("index", messages=error))
        else:
            flash(error)
            return render_template('admin_login.html', title='Получение прав администратора')
    else:
        return render_template('admin_login.html', title='Получение прав администратора')

@app.route('/logout')
def logout():
    session['login'] = None
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = str(request.form['password']).strip()
        chk_password = str(request.form['chk_password']).strip()
        error = None
        if password != chk_password:
            error = 'Пароли не совпадают'
            data = login
        if error is None:
            try:
                db.session.add(User(login=login, password=generate_password_hash(password)))
                db.session.flush()
            except exc.IntegrityError:
                db.session.rollback()
                error = f"Пользователь \"{login}\" уже зарегестрирован."
                data = ""
            else:
                db.session.commit()
                return redirect(url_for("login"))
        flash(error)
        return render_template('register.html', title='Регистрация', data=data)
    else:
        return render_template('register.html', title='Регистрация')

@app.route('/add_genre', methods=['GET', 'POST'])
def add_genre():
    if request.method == 'POST':
        name = request.form['name']
        try:
            db.session.add(Genre(name=name))
            db.session.flush()
        except exc.IntegrityError:
            db.session.rollback()
            error = f"Жанр \"{name}\" уже в БД."
        else:
            db.session.commit()
            error = f"Жанр \"{name}\" успешно добавлен."
            return redirect(url_for("index", messages=error))
        flash(error)
        return render_template('add_genre.html', title='Добавление жанра')
    else:
        return render_template('add_genre.html', title='Добавление жанра')

@app.route('/add_country', methods=['GET', 'POST'])
def add_country():
    if request.method == 'POST':
        name = request.form['name']
        try:
            db.session.add(Country(name=name))
            db.session.flush()
        except exc.IntegrityError:
            db.session.rollback()
            error = f"Страна \"{name}\" уже в БД."
        else:
            db.session.commit()
            error = f"Страна \"{name}\" успешно добавлена."
            return redirect(url_for("index", messages=error))
        flash(error)
        return render_template('add_country.html', title='Добавление страны')
    else:
        return render_template('add_country.html', title='Добавление страны')

@app.route('/add_actor', methods=['GET', 'POST'])
def add_actor():
    countries = Country.query.all()
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        bdate = request.form['bdate']
        country = request.form['countries_l']
        try:
            db.session.add(Actor(name=name, surname=surname, bdate=bdate, country=country))
            db.session.flush()
        except exc.IntegrityError:
            db.session.rollback()
            error = f"Актер с такими данными уже в базе данных."
        else:
            db.session.commit()
            error = f"Актер успешно добавлен."
            return redirect(url_for("index", messages=error))
        flash(error)
        return render_template('add_actor.html', title='Добавление актера', countries=countries)
    else:
        return render_template('add_actor.html', title='Добавление актера', countries=countries)

@app.route('/add_director', methods=['GET', 'POST'])
def add_director():
    countries = Country.query.all()
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        bdate = request.form['bdate']
        country = request.form['countries_l']
        try:
            db.session.add(Director(name=name, surname=surname, bdate=bdate, country=country))
            db.session.flush()
        except exc.IntegrityError:
            db.session.rollback()
            error = f"Режиссер с такими данными уже в базе данных."
        else:
            db.session.commit()
            error = f"Режиссер успешно добавлен."
            return redirect(url_for("index", messages=error))
        flash(error)
        return render_template('add_director.html', title='Добавление режиссера', countries=countries)
    else:
        return render_template('add_director.html', title='Добавление режиссера', countries=countries)

@app.route('/add_film', methods=['GET', 'POST'])
def add_film():
    actors = Actor.query.all()
    directors = Director.query.all()
    genres = Genre.query.all()
    countries = Country.query.all()
    if request.method == 'POST':
        actors_list = []
        directors_list = []
        genres_list = []
        countries_list = []
        title = request.form['name']
        rel_date = request.form['rel_date']
        description = request.form['description']
        for key, val in request.form.items():
            if key.startswith("actors_list_ids"):
                actors_list.append(val)
            elif key.startswith("directors_list_ids"):
                directors_list.append(val)
            elif key.startswith("genres_list_ids"):
                genres_list.append(val)
            elif key.startswith("countries_list_ids"):
                countries_list.append(val)
        error = None
        if not actors_list or not directors_list or not genres_list or not countries_list:
            error = 'Ошибка. Недостаточно данных для создания фильма.'
        if error is None:
            try:
                film = Film(name=title, year=rel_date, description=description)
                db.session.add(film)
                db.session.flush()
            except exc.IntegrityError:
                db.session.rollback()
                error = f"Фильм с такими данными уже есть в БД."
            else:
                film_id = film.id
                db.session.commit()
                for actor in actors_list:
                    db.session.add(Actor_in_film(act_id=actor, film_id=film_id))
                for director in directors_list:
                    db.session.add(Film_director(dir_id=director, film_id=film_id))
                for genre in genres_list:
                    db.session.add(Genre_in_film(film_id=film_id, genre_id=genre))
                for country in countries_list:
                    db.session.add(Film_by_country(film_id=film_id, country_id=country))
                db.session.commit()
                error = f"Фильм успешно добавлен."
                return redirect(url_for("index", messages=error))
        else:
            flash(error)
        return render_template('add_film.html', title='Добавление фильма', genres=genres, directors=directors,
                               actors=actors, countries=countries)
    else:
        return render_template('add_film.html', title='Добавление фильма', genres=genres, directors=directors,
                               actors=actors, countries=countries)

@app.route('/film/<id>', methods=['GET', 'POST'])
def film(id):
    current_film = Film.query.filter_by(id=id).first()
    genres = db.session.query(Genre_in_film.genre_id).filter_by(film_id=id).all()
    countries = db.session.query(Film_by_country.country_id).filter_by(film_id=id).all()
    actors_list = Actor_in_film.query.filter_by(film_id=id).all()
    directors_list = Film_director.query.filter_by(film_id=id).all()
    reviews = Review.query.filter_by(film_id=id).all()
    actors = [Actor.query.filter_by(id=a.act_id).first() for a in actors_list]
    directors = [Director.query.filter_by(id=d.dir_id).first() for d in directors_list]
    rate_list = rating_count(current_film.rating)
    user_review = Review.query.filter_by(film_id=id, user=g.user.login).first()
    have_reviews = False
    for r in reviews:
        if r.review_header:
            have_reviews = True
    if request.method == 'POST':
        review_title = request.form.get('title')
        review_text = request.form.get('description')
        for k,v in request.form.items():
            if k.startswith("rating") and v:
                film_rating = float(v)*2
        error = None
        if (review_title and not review_text) or (review_text and not review_title):
            error = 'Вы должны ввести и название и текст рецензии одновременно!'
        if error is None:
            try:
                past_review = Review.query.filter_by(film_id=id,user=g.user.login).first()
                if (past_review):
                    past_review.review_header = review_title
                    past_review.review_text = review_text
                else:
                    db.session.add(Review(film_id=id, rating=film_rating, review_header=review_title, review_text=review_text,user=g.user.login))
                    db.session.flush()
            except exc.IntegrityError:
                db.session.rollback()
                error = f"Этот пользователь уже написал рецензию к данному фильму."
            else:
                db.session.commit()
                reviews = Review.query.filter_by(film_id=id).all()
                full_rate = 0
                rated_users = 0
                for f in reviews:
                    rated_users+=1
                    full_rate+=f.rating
                if rated_users:
                    full_rate = full_rate/rated_users
                current_film = Film.query.filter_by(id=id).first()
                current_film.rating = full_rate
                db.session.commit()
                current_film = Film.query.filter_by(id=id).first()
                rate_list = rating_count(current_film.rating)
                user_review = Review.query.filter_by(film_id=id, user=g.user.login).first()
                have_reviews = False
                for r in reviews:
                    if r.review_header:
                        have_reviews = True
                return render_template('film.html', title=current_film.name, film=current_film,
                                       countries=countries,
                                       genres=genres, actors=actors, directors=directors, rating=rate_list,
                                       reviews=reviews, user_review=user_review, have_reviews=have_reviews)
        else:
            return render_template('film.html', messages=error, title=current_film.name, film=current_film, countries=countries,
                               genres=genres, actors=actors, directors=directors, rating=rate_list, reviews=reviews,
                                   user_review=user_review, have_reviews=have_reviews)
    else:
        return render_template('film.html', title=current_film.name, film=current_film, countries=countries,
                           genres=genres, actors=actors, directors=directors, rating=rate_list, reviews=reviews,
                               user_review=user_review, have_reviews=have_reviews)

@app.route('/search_film', methods=['GET', 'POST'])
def search_film():
    films = Film.query.all()
    genres = {}
    countries = {}
    favs = set()
    all_films_genres = []
    all_films_countries = []
    years_set = set()
    for f in films:
        genres_list = Genre_in_film.query.filter_by(film_id = f.id).all()
        countries_list = Film_by_country.query.filter_by(film_id = f.id).all()
        film_genres = []
        film_countries = []
        if User_films.query.filter_by(film_id=f.id, user=g.user.login).first():
            favs.add(f.id)
        for ge in genres_list:
            film_genres.append(ge.genre_id)
            all_films_genres.append(ge.genre_id)
        for c in countries_list:
            film_countries.append(c.country_id)
            all_films_countries.append(c.country_id)
        genres[f.id] = film_genres
        countries[f.id] = film_countries
        years_set.add(f.year)
    min_year = min(years_set)
    max_year = max(years_set)
    if request.method == 'POST':
        if 'to_favs' in request.form:
            film_id = request.form['to_favs']
            try:
                db.session.add(User_films(film_id=film_id, user=g.user.login))
                db.session.flush()
            except exc.IntegrityError:
                db.session.rollback()
            else:
                db.session.commit()
                favs.add(int(film_id))
            return render_template('search_film.html', title='Поиск фильмов', films=films, countries=countries,
                                   genres=genres, genres_list=set(all_films_genres),
                                   countries_list=set(all_films_countries), min_year=min_year, max_year=max_year, favs=favs)
        elif 'from_favs' in request.form:
            film_id = request.form['from_favs']
            try:
                db.session.delete(User_films.query.filter_by(film_id=film_id, user=g.user.login).first())
                db.session.flush()
            except exc.IntegrityError:
                db.session.rollback()
            else:
                db.session.commit()
                favs.remove(int(film_id))
            return render_template('search_film.html', title='Поиск фильмов', films=films, countries=countries,
                                   genres=genres, genres_list=set(all_films_genres),
                                   countries_list=set(all_films_countries), min_year=min_year, max_year=max_year, favs=favs)
        else:
            chosen_films = set()
            chosen_genres_list = []
            chosen_countries_list = []
            min_date = request.form['min_date']
            max_date = request.form['max_date']
            name = request.form.get('film_name').lower()
            min_date = (int(min_date) if min_date else 0)
            max_date = (int(max_date) if max_date else 0)
            if min_date and max_date and min_date > max_date:
                min_date, max_date = max_date, min_date
            for key, val in request.form.items():
                if key.startswith("genres_list_ids"):
                    chosen_genres_list.append(val)
                elif key.startswith("countries_list_ids"):
                    chosen_countries_list.append(val)
            for f in films:
                if (f.name.lower()+", year: "+ str(f.year)).startswith(name):
                    for ge in genres[f.id]:
                        if not chosen_genres_list or ge in chosen_genres_list:
                            for c in countries[f.id]:
                                if not chosen_countries_list or c in chosen_countries_list:
                                    if (not min_date and not max_date) or (f.year >= min_date and not max_date) or (
                                            max_date >= f.year and not min_date) or (min_date <= f.year <= max_date):
                                        chosen_films.add(f)
                                        continue
            order = request.form.get('rating')
            chosen_films = list(chosen_films)
            if order == 'asc':
                chosen_films.sort(key=lambda x: x.rating, reverse=False)
            elif order == 'desc':
                chosen_films.sort(key=lambda x: x.rating, reverse=True)
            return render_template('search_film.html', title='Поиск фильмов', films=chosen_films, countries=countries,
                                       genres=genres, genres_list=set(all_films_genres),
                                       countries_list=set(all_films_countries), min_year=min_year, max_year=max_year, favs=favs)
    else:
        return render_template('search_film.html', title='Поиск фильмов', films=films, countries=countries,
                               genres=genres, genres_list=set(all_films_genres),
                               countries_list=set(all_films_countries), min_year=min_year, max_year=max_year, favs=favs)

@app.route('/user_reviews', methods=['GET', 'POST'])
def user_reviews():
    films = {}
    ratings = {}
    reviews = Review.query.filter_by(user=g.user.login).all()
    for r in reviews:
        films[r.id] = Film.query.filter_by(id=r.film_id).first()
        ratings[r.id] = rating_count(r.rating)
    if request.method == 'POST':
        rev_id = request.form['del_review']
        try:
            review_to_del=Review.query.filter_by(id=rev_id).first()
            film_id = review_to_del.film_id
            db.session.delete(review_to_del)
            db.session.flush()
        except exc.IntegrityError:
            db.session.rollback()
        else:
            db.session.commit()
            reviews = Review.query.filter_by(film_id=film_id).all()
            full_rate = 0
            rated_users = 0
            for f in reviews:
                rated_users += 1
                full_rate += f.rating
            if rated_users:
                full_rate = full_rate / rated_users
            current_film = Film.query.filter_by(id=film_id).first()
            current_film.rating = full_rate
            db.session.commit()
            reviews = Review.query.filter_by(user=g.user.login).all()
            return render_template('user_reviews.html', title='Мои рецензии', reviews=reviews, films=films, ratings=ratings)
        return render_template('user_reviews.html', title='Мои рецензии', reviews=reviews, films=films, ratings=ratings)
    else:
        return render_template('user_reviews.html', title='Мои рецензии', reviews=reviews, films=films, ratings=ratings)

@app.route('/user_films', methods=['GET', 'POST'])
def user_films():
    favs = User_films.query.filter_by(user=g.user.login).all()
    films = set()
    for f in favs:
        films.add(Film.query.filter_by(id=f.film_id).first())
    genres = {}
    countries = {}
    for f in films:
        genres_list = Genre_in_film.query.filter_by(film_id=f.id).all()
        countries_list = Film_by_country.query.filter_by(film_id=f.id).all()
        film_genres = []
        film_countries = []
        for ge in genres_list:
            film_genres.append(ge.genre_id)
        for c in countries_list:
            film_countries.append(c.country_id)
        genres[f.id] = film_genres
        countries[f.id] = film_countries
    if request.method == 'POST':
        film_id = request.form['from_favs']
        try:
            db.session.delete(User_films.query.filter_by(film_id=film_id, user=g.user.login).first())
            db.session.flush()
        except exc.IntegrityError:
            db.session.rollback()
        else:
            db.session.commit()
            films.remove(Film.query.filter_by(id=film_id).first())
        return render_template('user_films.html', title='Избранные фильмы', films=films, countries=countries,
                                   genres=genres)
    else:
        return render_template('user_films.html', title='Избранные фильмы', films=films, countries=countries,
                               genres=genres)
@app.route('/actor/<actor_id>', methods=['GET', 'POST'])
def actor(actor_id):
    actor = Actor.query.filter_by(id=actor_id).first()
    act_films = Actor_in_film.query.filter_by(act_id=actor_id).all()
    films = set()
    for f in act_films:
        films.add(Film.query.filter_by(id=f.film_id).first())
    if request.method == 'POST':
        return render_template('actor.html', title='Персональная страница актера', films=films, actor=actor)
    else:
        return render_template('actor.html', title='Персональная страница актера', films=films, actor=actor)

@app.route('/director/<director_id>', methods=['GET', 'POST'])
def director(director_id):
    director = Director.query.filter_by(id=director_id).first()
    dir_films = Film_director.query.filter_by(dir_id=director_id).all()
    films = set()
    for f in dir_films:
        films.add(Film.query.filter_by(id=f.film_id).first())
    if request.method == 'POST':
        return render_template('director.html', title='Персональная страница режиссера', films=films, director=director)
    else:
        return render_template('director.html', title='Персональная страница режиссера', films=films, director=director)

def rating_count(rating):
    rate_list = ['' for i in range(11)]
    if rating == 10:
        rate_list[10] = 'checked'
    elif 9<=rating<10:
        rate_list[9] = 'checked'
    elif 8<=rating<9:
        rate_list[8] = 'checked'
    elif 7<=rating<8:
        rate_list[7] = 'checked'
    elif 6<=rating<7:
        rate_list[6] = 'checked'
    elif 5<=rating<6:
        rate_list[5] = 'checked'
    elif 4<=rating<5:
        rate_list[4] = 'checked'
    elif 3<=rating<4:
        rate_list[3] = 'checked'
    elif 2<=rating<3:
        rate_list[2] = 'checked'
    elif 1<=rating<2:
        rate_list[1] = 'checked'
    else:
        rate_list[0] = 'checked'
    return rate_list


