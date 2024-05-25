# app.py
from flask import Flask, render_template, request, redirect, url_for
from models import db, Movie, Showtime, Booking

app = Flask(__name__)
user = "root"
pin = "root"
host = "localhost"
db_name = "movie_db"

# Configuring database URI
# app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{pin}@{host}/{db_name}"
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{pin}@{host}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/movie/<int:movie_id>')
def show_movie(movie_id):
    movie = Movie.query.get(movie_id)
    return render_template('movies.html', movie=movie)

@app.route('/showtime/<int:showtime_id>', methods=['GET', 'POST'])
def book_showtime(showtime_id):
    showtime = Showtime.query.get(showtime_id)
    if request.method == 'POST':
        customer_name = request.form['name']
        seats = int(request.form['seats'])
        booking = Booking(customer_name=customer_name, showtime_id=showtime.id, seats=seats)
        db.session.add(booking)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('booking.html', showtime=showtime)

@app.route('/showtime/<int:showtime_id>/status')
def booking_status(showtime_id):
    showtime = Showtime.query.get(showtime_id)
    bookings = showtime.bookings
    return render_template('status.html', showtime=showtime, bookings=bookings)

if __name__ == '__main__':
    app.run(debug=True)
