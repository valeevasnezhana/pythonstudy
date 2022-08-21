import typing as tp
import sqlite3
from pypika import Query, Table, Order


class DataBaseHandler:
    def __init__(self, sqlite_database_name: str):
        """
        Initialize all the context for working with database here
        :param sqlite_database_name: path to the sqlite3 database file
        """
        self.connection = sqlite3.connect(sqlite_database_name)

    def _execute(self, query: Query):
        cursor = self.connection.cursor()
        cursor.execute(str(query))
        return cursor.fetchall()

    def get_most_expensive_track_names(self, number_of_tracks: int) -> tp.Sequence[tp.Tuple[str]]:
        """
        Return the sequence of track names sorted by UnitPrice descending.
        If the price is the same, sort by TrackId ascending.
        :param number_of_tracks: how many track names should be returned
        keywords: SELECT, ORDER BY, LIMIT
        :return:
        """
        tracks = Table('tracks')
        query = Query.from_(tracks)\
            .orderby(tracks.UnitPrice, order=Order.desc)\
            .orderby(tracks.TrackId, order=Order.asc)\
            .select('Name')\
            .limit(number_of_tracks)
        return self._execute(query)

    def get_tracks_of_given_genres(self, genres: tp.Sequence[str], number_of_tracks: int) -> tp.Sequence[tp.Tuple[str]]:
        """
        Return the sequence of track names that have one of the given genres
        sort ascending by track duration and limit by number_of_tracks
        :param number_of_tracks:
        :param genres:
        keywords: JOIN, WHERE, IN
        :return:
        """
        tracks = Table('tracks')
        genres_table = Table('genres')
        query = Query.from_(tracks)\
            .inner_join(genres_table)\
            .using('GenreId')\
            .where(genres_table.Name.isin(genres))\
            .orderby(tracks.Milliseconds, order=Order.asc)\
            .select(tracks.Name)\
            .limit(number_of_tracks)
        return self._execute(query)

    def get_tracks_that_belong_to_playlist_found_by_name(self, name_needle: str) -> tp.Sequence[tp.Tuple[str, str]]:
        """
        Return a sequence of track names and playlist names such that the track belongs to the playlist and
        the playlist's name contains `name_needle` (case sensitive).
        If the track belongs to more than one suitable playlist it
        should occur in the result for each playlist, but not just once
        :param name_needle:
        keywords: JOIN, WHERE, LIKE
        :return:
        """
        tracks = Table('tracks')
        playlists = Table('playlists')
        playlist_track = Table('playlist_track')
        query = Query.from_(tracks)\
            .inner_join(playlist_track).using('TrackId')\
            .inner_join(playlists).using('PlaylistId')\
            .where(playlists.Name.like(f'%{name_needle}%'))\
            .select(tracks.Name, playlists.Name)
        return self._execute(query)

    def teardown(self) -> None:
        """
        Cleanup everything after working with database.
        Do anything that may be needed or leave blank
        :return:
        """
        self.connection.close()
