from flask import Flask
from flask import render_template
from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
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


# Admin
class AdminView(AdminIndexView):
    @expose('/')
    def index(self):
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

    return render_template("index.html")


@app.route("/history")
def history():
    songs = Song.query.all()
    return render_template("history.html", songs=songs)


@app.route("/song/<song_id>")
def song(song_id):
    song = Song.query.get_or_404(song_id)
    return render_template("detail.html", song=song)


if __name__ == "__main__":
    db.create_all()
    app.run()
