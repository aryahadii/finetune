import json
import yaml
from os import path
from collections import defaultdict

import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyAPI:

    def __init__(self) -> None:
        with open('client_auth.yaml', 'r') as client_auth:
            y = yaml.safe_load(client_auth)
            self.client_id = y['client_id']
            self.client_secret = y['client_secret']
            self.redirect_uri = y['redirect_uri']

        self.api = spotipy.Spotify(
            auth_manager=SpotifyOAuth(client_id=self.client_id,
                                      client_secret=self.client_secret,
                                      redirect_uri=self.redirect_uri,
                                      scope="user-library-modify",
                                      )
        )

    def remove_user_saved_tracks(self, tracks_uri):
        for i in range(0, len(tracks_uri), 50):  # Spotify has 50 items limit per request
            self.api.current_user_saved_tracks_delete(
                tracks=tracks_uri[i:i+50])


class Track:

    def __init__(self, name, artist, uri=None) -> None:
        self.name = name
        self.artist = artist
        self.uri = uri

    def __str__(self) -> str:
        return f'{self.artist} - {self.name} [{self.uri}]'

    def __eq__(self, other):
        if not isinstance(other, Track):
            return False
        if self.uri and other.uri:
            return self.uri == other.uri
        return self.name == other.name and self.artist == other.artist

    def __hash__(self):
        return hash((self.name, self.artist))


class SpotifyData:

    def __init__(self, spotify_data_export_dir) -> None:
        self.data_dir = spotify_data_export_dir

    def play_count(self):
        play_count = defaultdict(lambda: 0)

        history = self._streaming_history()
        for track in history:
            key = Track(name=track['trackName'], artist=track['artistName'])
            play_count[key] += 1

        return play_count

    def _streaming_history(self):
        history = []

        streaming_history_file_index = 0
        while True:
            filepath = path.join(
                self.data_dir, f'StreamingHistory{streaming_history_file_index}.json')
            if not path.exists(filepath):
                break

            history += self._load_streaming_history_file(filepath)
            streaming_history_file_index += 1

        return history

    def _load_streaming_history_file(self, filepath):
        with open(filepath, 'r') as streaming_history_file:
            streaming_history = json.load(streaming_history_file)
            return streaming_history

    def library(self):
        tracks = []

        library_filepath = path.join(self.data_dir, 'YourLibrary.json')
        with open(library_filepath, 'r') as library_file:
            library = json.load(library_file)

            for track in library['tracks']:
                tracks.append(Track(
                    name=track['track'],
                    artist=track['artist'],
                    uri=track['uri'],
                ))

        return tracks

    def _track_key(self, name, artist):
        return f"{artist} - {name}"

    def played_songs_in_library(self, played_count_threshold=None):
        library = self.library()
        play_count = self.play_count()

        counted_library = []
        for track in library:
            if not played_count_threshold or play_count[track] < played_count_threshold:
                counted_library.append((track, play_count[track]))
        return sorted(counted_library, key=lambda t: t[1])
