import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sqlite3
import json


class GetData:
    def __init__(self):
        self.adj_dict = {}
        self.coldplay_uri = 'spotify:artist:4gzpq5DPGxSnKTe4SA8HAU'
        self.scope = "user-library-read"
        self.client = os.environ.get('SPOTIPY_CLIENT_ID')
        self.secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scope, client_id=self.client,
                                                                 client_secret=self.secret))
        self.artists = []
        self.artist_names = []
        self.path = []
        self.songs = []
        self.conn = sqlite3.connect('adj_list.db')
        self.c = self.conn.cursor()

    def get_coldplay_relations(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS adj_list (
                        artist text,
                        related blob
                        )""")

        results = self.spotify.artist_albums(self.coldplay_uri, album_type='album,single')
        print("Accessed API")

        albums = results['items']

        while results['next']:
            results = self.spotify.next(results)
            albums.extend(results['items'])

        tracks = []
        for album in albums:
            results = self.spotify.album_tracks(album['external_urls']['spotify'])
            album_tracks = results['items']
            tracks.extend(album_tracks)

            while results['next']:
                results = self.spotify.next(results)
                tracks.extend(results['items'])

        for track in tracks:
            if len(track['artists']) > 1:
                self.artists.extend(track['artists'])
            if '(feat.' in track['name']:
                name = track['name']
                words = name.split('(feat.')
                name = ' '.join(words[2:])[:-1]
                if name not in self.artist_names:
                    self.artist_names.append(name)
            elif '(with' in track['name']:
                name = track['name']
                words = name.split('(with')
                name = ' '.join(words[2:])[:-1]
                if name not in self.artist_names:
                    self.artist_names.append(name)

        for artist in self.artists:
            if artist['name'] not in self.artist_names and artist['name'] != 'Coldplay':
                self.artist_names.append(artist['name'])

        blob = json.dumps(self.artist_names)
        self.c.execute("SELECT * FROM adj_list WHERE artist=?", ('Coldplay',))
        data = self.c.fetchone()
        if not data:
            self.c.execute("INSERT INTO adj_list VALUES ('Coldplay', ?)", [blob])
            self.conn.commit()

    def add_layer(self):
        print("Adding layer")
        for artist in self.artist_names:
            try:
                result = self.spotify.search(artist, type='artist')
                current_artist = result['artists']['items'][0]
            except spotipy.exceptions.SpotifyException:
                continue
            followers = current_artist['followers']['total']
            if followers is not None and followers > 15000:
                artist_uri = current_artist['uri']

                results = self.spotify.artist_albums(artist_uri, album_type='album,single')
                albums = results['items']

                while results['next']:
                    results = self.spotify.next(results)
                    albums.extend(results['items'])

                tracks = []
                for album in albums:
                    results = self.spotify.album_tracks(album['external_urls']['spotify'])
                    album_tracks = results['items']
                    tracks.extend(album_tracks)

                    while results['next']:
                        results = self.spotify.next(results)
                        tracks.extend(results['items'])

                self.artists = []
                self.artist_names = []
                for track in tracks:
                    if len(track['artists']) > 1:
                        self.artists.extend(track['artists'])
                    if 'feat' in track['name'] or '(with' in track['name']:
                        name = track['name']
                        words = name.split()
                        name = ' '.join(words[2:])[:-1]

                for a in self.artists:
                    if a['name'] not in self.artist_names and a['name'] != artist:
                        current_artist = self.spotify.artist(a['uri'])
                        followers = current_artist['followers']['total']
                        if followers is not None and followers > 15000:
                            self.artist_names.append(a['name'])

                # self.adj_dict.update({artist: self.artist_names})
                blob = json.dumps(self.artist_names)
                self.c.execute("SELECT * FROM adj_list WHERE artist=?", (artist,))
                data = self.c.fetchone()
                if not data:
                    self.c.execute("INSERT INTO adj_list VALUES (?, ?)", [artist, blob])
                    self.conn.commit()
                    print("added")

    def bfs(self):
        edge_to = {}
        dist = {}
        marked = {}
        queue = []
        print("Initializing breadth-first-search")
        self.c.execute("SELECT artist from adj_list")
        artists = self.c.fetchall()
        for node in artists:
            edge_to[node[0]] = None
            marked[node[0]] = False
            dist[node[0]] = -1
            self.c.execute("SELECT * FROM adj_list WHERE artist=?", (node))
            children = json.loads(self.c.fetchone()[1])
            for child in children:
                edge_to[child] = None
                marked[child] = False
                dist[child] = -1

        queue.append('Coldplay')
        marked['Coldplay'] = True

        print("Beginning BFS")
        while queue:
            v = queue.pop(0)
            self.c.execute("SELECT artist from adj_list")
            artists = self.c.fetchall()
            artists = [item for item in artists if item[0] == v]
            if artists:
                self.c.execute("SELECT * FROM adj_list WHERE artist=?", (v,))
                children = json.loads(self.c.fetchone()[1])
                for vert in children:
                    if marked[vert]:
                        continue
                    else:
                        queue.append(vert)
                        edge_to[vert] = v
                        marked[vert] = True
                        dist[vert] = dist[v] + 1

        v = 'Kendrick Lamar'
        chosen_artist = v
        if v in marked.keys() and marked[v] is True:
            self.path.append(v)
            print("Creating path")
            while edge_to[v]:
                self.path.append(edge_to[v])
                v = edge_to[v]
        else:
            print("No path")

        if self.path:
            print(f"Coldplay is connected to {chosen_artist}!")
            self.path.reverse()

            for i in range(len(self.path) - 1):
                result = self.spotify.search(self.path[i] + " " + self.path[i + 1], type='track')
                for i in range(5):
                    if 'Remix' not in result['tracks']['items'][i]['name']:
                        song = result['tracks']['items'][i]['name']
                        self.songs.append(song)
                        break

            print(self.path)
            print(self.songs)
