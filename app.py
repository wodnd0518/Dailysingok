from flask import Flask
from flask import request
from flask import render_template
from flask import Response
from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'true'
db = SQLAlchemy(app)


# Model
class Song(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    artist = db.Column(db.String(255))
    picture = db.Column(db.String(255))
    youtube = db.Column(db.String(255))
    created_at = db.Column(db.DateTime())
    comment = db.Column(db.String(255))
    genre = db.Column(db.String(255))


def check_auth(username, password):
    return username == 'wodnd0518' and password == '000518'


def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


# Admin
class AdminView(AdminIndexView):
    @expose('/')
    def index(self):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return super(AdminView, self).index()


class SongView(ModelView):
    column_list = ('id', 'title', 'artist', 'created_at',)

    def __init__(self, session, **kwargs):
        super(SongView, self).__init__(Song, session, **kwargs)

admin = Admin(app, name="DailySingok", index_view=AdminView())
admin.add_view(SongView(db.session, name='Song'))


# View
@app.route("/")
def index():
    today = datetime.date.today().strftime("%Y-%m-%d")
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    today_song = Song.query \
        .filter(Song.created_at.between(today, tomorrow)) \
        .first()
    if today_song is None:
        song = Song.query \
            .order_by(Song.created_at.desc()) \
            .first()
        print song.id
    else:
        song = today_song
    return render_template("index.html", song=song)


@app.route("/history")
def history():
    songs = Song.query \
        .order_by(Song.created_at) \
        .all()
    return render_template("history.html", songs=songs)


@app.route("/song/<song_id>")
def song(song_id):
    song = Song.query.get_or_404(song_id)
    return render_template("detail.html", song=song)


if __name__ == "__main__":
    db.create_all()
    app.run()
