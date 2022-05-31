import os
import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from get_data import GetData

gd = GetData()

gd.get_coldplay_relations()
for i in range(2):
    gd.add_layer()

gd.bfs()


# scope = "user-library-read"
#
# client = os.environ.get('SPOTIPY_CLIENT_ID')
# secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
# spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client, client_secret=secret))
#
# coldplay_uri = 'spotify:artist:4gzpq5DPGxSnKTe4SA8HAU'
#
#
# results = spotify.artist_albums(coldplay_uri, album_type='album,single')
# print("Accessed API")
#
# albums = results['items']
#
# while results['next']:
#     results = spotify.next(results)
#     albums.extend(results['items'])
#
# tracks = []
# for album in albums:
#     results = spotify.album_tracks(album['external_urls']['spotify'])
#     album_tracks = results['items']
#     tracks.extend(album_tracks)
#
#     while results['next']:
#         results = spotify.next(results)
#         tracks.extend(results['items'])
#
# artists = []
# cleaned_artists_one = []
# for track in tracks:
#     if 'Remix' not in track['name']:
#         if len(track['artists']) > 1:
#             artists.extend(track['artists'])
#         if '(feat.' in track['name']:
#             name = track['name']
#             words = name.split('(feat.')
#             name = ' '.join(words[2:])[:-1]
#             if name not in cleaned_artists_one:
#                 cleaned_artists_one.append(name)
#         elif '(with' in track['name']:
#             name = track['name']
#             words = name.split('(with')
#             name = ' '.join(words[2:])[:-1]
#             if name not in cleaned_artists_one:
#                 cleaned_artists_one.append(name)
#
# for artist in artists:
#     if artist['name'] not in cleaned_artists_one and artist['name'] != 'Coldplay':
#         cleaned_artists_one.append(artist['name'])
#
#
# path = []
#
#
# adj_dict = {"Coldplay": cleaned_artists_one}
#
# for artist in cleaned_artists_one:
#     try:
#         result = spotify.search(artist, type='artist')
#     except:
#         continue
#     try:
#         current_artist = result['artists']['items'][0]
#     except:
#         continue
#     artist_uri = current_artist['uri']
# #
#     results = spotify.artist_albums(artist_uri, album_type='album,single')
#     albums = results['items']
#
#     while results['next']:
#         results = spotify.next(results)
#         albums.extend(results['items'])
#
#     tracks = []
#     for album in albums:
#         results = spotify.album_tracks(album['external_urls']['spotify'])
#         album_tracks = results['items']
#         tracks.extend(album_tracks)
#
#         while results['next']:
#             results = spotify.next(results)
#             tracks.extend(results['items'])
#
#     artists = []
#     cleaned_artists_two = []
#     for track in tracks:
#         if len(track['artists']) > 1:
#             if 'Remix' not in track['name']:
#                 artists.extend(track['artists'])
#         if 'feat' in track['name'] or '(with' in track['name']:
#             name = track['name']
#             words = name.split()
#             name = ' '.join(words[2:])[:-1]
#
#     for a in artists:
#         if a['name'] not in cleaned_artists_two and a['name'] != artist:
#             cleaned_artists_two.append(a['name'])
#
#     # print(cleaned_artists_two)
#     adj_dict.update({artist: cleaned_artists_two})
#
# for artist in cleaned_artists_two:
#     try:
#         result = spotify.search(artist, type='artist')
#     except:
#         pass
#     try:
#         current_artist = result['artists']['items'][0]
#     except:
#         pass
#     artist_uri = current_artist['uri']
#
#     results = spotify.artist_albums(artist_uri, album_type='album,single')
#     albums = results['items']
#
#     while results['next']:
#         results = spotify.next(results)
#         albums.extend(results['items'])
#
#     tracks = []
#     for album in albums:
#         results = spotify.album_tracks(album['external_urls']['spotify'])
#         album_tracks = results['items']
#         tracks.extend(album_tracks)
#
#         while results['next']:
#             results = spotify.next(results)
#             tracks.extend(results['items'])
#
#     artists = []
#     cleaned_artists_three = []
#     for track in tracks:
#         if len(track['artists']) > 1:
#             if 'Remix' not in track['name']:
#                 artists.extend(track['artists'])
#         if 'feat' in track['name'] or '(with' in track['name']:
#             name = track['name']
#             words = name.split()
#             name = ' '.join(words[2:])[:-1]
#
#     for a in artists:
#         if a['name'] not in cleaned_artists_three and a['name'] != artist:
#             cleaned_artists_three.append(a['name'])
#
#     adj_dict.update({artist: cleaned_artists_three})


# edge_to = {}
# dist = {}
# marked = {}
# queue = []
#
# print("Initializing breadth-first-search")
# for node in adj_dict.keys():
#     edge_to[node] = None
#     marked[node] = False
#     dist[node] = -1
#     for child in adj_dict[node]:
#         edge_to[child] = None
#         marked[child] = False
#         dist[child] = -1
#
# queue.append(list(adj_dict.keys())[0])
# marked[list(adj_dict.keys())[0]] = True
#
# print("Beginning BFS")
# while queue:
#     v = queue.pop(0)
#     if v in adj_dict:
#         for vert in adj_dict[v]:
#             if marked[vert]:
#                 continue
#             else:
#                 queue.append(vert)
#                 edge_to[vert] = v
#                 marked[vert] = True
#                 dist[vert] = dist[v] + 1
#
#
# v = 'J. Cole'
# chosen_artist = v
# if v in marked.keys() and marked[v] is True:
#     path.append(v)
#     print("Creating path")
#     while edge_to[v]:
#         path.append(edge_to[v])
#         v = edge_to[v]
# else:
#     print("No path")


# if path:
#     print(f"Coldplay is connected to {chosen_artist}!")
#     path.reverse()
#     songs = []
#
#     for i in range(len(path) - 1):
#         result = spotify.search(path[i] + " " + path[i + 1], type='track')
#         print(result)
#         for i in range(5):
#             if 'Remix' not in result['tracks']['items'][i]['name']:
#                 song = result['tracks']['items'][i]['name']
#                 songs.append(song)
#                 break
#     print(path)
#     print(songs)





