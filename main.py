import sqlalchemy
from random import randint

engine = sqlalchemy.create_engine('postgresql://shadov:admin@localhost:5432/shadov_base')
engine

connection = engine.connect()
artists = ['artist' + str(i) for i in range(1, 8)] + ['name 3 word']
genres = ['genre' + str(i) for i in range(1, 6)]
albums = ['album' + str(i) for i in range(1, 9)]
tracks = ['track' + str(i) for i in range(1, 15)] + ['мой 2007', 'in my heart']
collections = ['collection' + str(i) for i in range(1, 9)]


def add_table():
    sel = connection.execute("""
    drop table Song cascade;
    drop table Collection cascade;
    drop table SingerGenre cascade;
    drop table SingerAlbum cascade;
    drop table Album cascade;
    drop table Singer cascade;
    drop table Genre cascade;
    drop table SongCollection cascade;
    """)
    print("БД Удалена")

    sel = connection.execute("""create table if not exists Genre (
        id serial primary key,
        name VARCHAR(50) not null unique
    );

    create table if not exists Singer (
        id serial primary key,
        name VARCHAR(50) not null unique
    );

    create table if not exists SingerGenre (
    singer_id integer references Singer(id),
    genre_id integer references Genre(id),
    constraint pk primary key (singer_id, genre_id)
    );

    create table if not exists Album(
        id serial primary key,
        name VARCHAR(150) not null unique,
        year integer
    );

    create table if not exists SingerAlbum (
    singer_id integer references Singer(id),
    album_id integer references Album(id),
    constraint hz primary key (singer_id, album_id)
    );

    create table if not exists Collection (
        id serial primary key,
        name VARCHAR(150) not null unique,
        year integer
    );

    create table if not exists Song (
        id serial primary key,
        album_id integer not null references album(id),
        name VARCHAR(150) not null unique,
        timing numeric
    );

    create table if not exists SongCollection (
        song_id integer references Song(id),
        collection_id integer references Collection(id),
        constraint xz primary key (song_id, collection_id)
    );
    """)

    print('БД создана')


def add_genre():
    for genre in genres:
        sel = connection.execute("INSERT INTO genre(name) VALUES('" + genre + "');")
    print('Жанры записаны')


def add_artist():
    for artist in artists:
        sel = connection.execute("INSERT INTO singer(name) VALUES('" + artist + "');")
    print("Артисты добавлены")


def add_artist_genre():  # костыль - каждому артисту по одному жанру, чтобы не случалось не соблюдения уникальности записей
    for i in range(1, 9):
        sel = connection.execute(
            "INSERT INTO singergenre VALUES (" + str(i) + "," + str(randint(1, len(genres))) + ");")
    print("Артисты - жанры заполнены")


def add_album():
    for album in albums:
        sel = connection.execute(
            "INSERT INTO album(name, year) VALUES('" + album + "'," + str(randint(2015, 2021)) + ");")
    print("Альбомы заполнены")


def add_collection():
    for collection in collections:
        sel = connection.execute(
            "INSERT INTO collection(name, year) VALUES('" + collection + "'," + str(randint(2015, 2021)) + ");")
    print("Сборники заполнены")


def add_tracks():
    for song in tracks:
        sel = connection.execute("INSERT INTO song(album_id, name, timing)  "
                                 "VALUES(" + str(randint(1, len(albums))) + ",'" + song + "'," + str(
            randint(2, 5)) + '.' + str(randint(1, 60)) + ");")

    print("Треки заполнены")


def add_singer_album():
    for i in range(1, len(artists)):
        sel = connection.execute(
            "INSERT INTO singeralbum VALUES (" + str(i) + "," + str(randint(1, len(albums))) + ");")
    print("Артисты - альбомы заполнены")


def add_song_collection():
    for i in range(1, len(tracks)):
        sel = connection.execute(
            "INSERT INTO songcollection VALUES (" + str(i) + "," + str(randint(1, len(collections))) + ");")
    print("Песни - сборники заполнены")


add_table()
add_genre()
add_artist()
add_artist_genre()
add_album()
add_collection()
add_tracks()
add_singer_album()
add_song_collection()

print('_______________________________________')
print('Альбомы из 2018:', connection.execute("SELECT name, year FROM album WHERE year = 2018;").fetchall())
print('Самый длинный трек:', connection.execute("SELECT name, timing FROM song ORDER BY timing DESC;").fetchone())
print('Треки длиной более 3.5 минуты:', connection.execute("SELECT name FROM song WHERE timing > 3.5;").fetchall())
print('Сборники с 2018 по 2020:',
      connection.execute("SELECT name FROM collection WHERE year BETWEEN 2018 AND 2020;").fetchall())
print('Исполнители из 1 слова:', connection.execute("SELECT name FROM singer WHERE name NOT LIKE '%% %%';").fetchall())
print('Треки с my/мой:',
      connection.execute("SELECT name FROM song WHERE name LIKE '%%мой%%' OR name LIKE '%%my%%';").fetchall())