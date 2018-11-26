import os
from spotipy import Spotify
from spotipy.util import prompt_for_user_token
import urllib

# sophia
CLIENT_ID = '0e7ea227ef7d407b8bf47a4c545adb3c'
CLIENT_SECRET = '267e96c4713f46d4885a4ea6a099ead4'
USERNAME = 'al321rltkr20p7oftb0i801lk'
# USERNAME = 'd6w8pm7psjnzjdwinyblm1ll4'
# USERNAME = 'hunterlum'
# USERNAME = 'firetrail'

# # colin
# CLIENT_ID = '4698619dc1854dd0a7d8f84b4d8dbf08'
# CLIENT_SECRET = '72b2599e6b314c1f88714a1b8b6afbb4'
# USERNAME = 'd6w8pm7psjnzjdwinyblm1ll4'

token = prompt_for_user_token(username=USERNAME, scope='user-library-read user-top-read playlist-modify-private', client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://www.google.com")
spotify = Spotify(auth=token)

def search(user_query, data_folder):
    query = {}
    for (track, artist) in user_query:
        search_query = "artist:{} track:{}".format(artist, track)
        results = spotify.search(q=search_query, type="track")
        print("searching for artist : {}, track : {} ...".format(artist, track), end="")
        try:
            song = results['tracks']['items'][0]
            mp3_file_path = "{}{}.mp3".format(data_folder, song["id"])
            query[song['id']] = (song['name'], song['artists'])
            if song['preview_url'] is not None:
                urllib.request.urlretrieve(song['preview_url'], mp3_file_path)
            print("done!")
        except Exception as e:
            print("Error: [{}] :(".format(e))
    print()
    return query

def downloadMP3(url, id, data_folder):
    mp3_file_path = "{}{}.mp3".format(data_folder, id)
    if not os.path.exists(mp3_file_path) and url is not None:
        urllib.request.urlretrieve(url, mp3_file_path)

def get_user_library(data_folder):
    user_library = {}
    playlists = spotify.current_user_playlists(limit=50)
    for playlist in playlists['items']:
        print(playlist['name'])
        print('  total tracks', playlist['tracks']['total'])
        
        results = spotify.user_playlist(USERNAME, playlist['id'], fields="tracks,next")
        tracks = results['tracks']
        
        for item in tracks['items']:
            track = item['track']
            user_library[track['id']] = (track['name'], track['artists']) # id = name, artist
            downloadMP3(track['preview_url'], track['id'], data_folder)

        while tracks['next']:
            tracks = spotify.next(tracks)
            for item in tracks['items']:
                track = item['track']
                user_library[track['id']] = (track['name'], track['artists']) # id = name, artist
                downloadMP3(track['preview_url'], track['id'], data_folder)

    #Get user's top tracks
    results = spotify.current_user_top_tracks(limit = 50) # Add user top tracks
    for item in results['items']:
        track = item
        user_library[track['id']] = (track['name'], track['artists'])  # id = name, artist
        downloadMP3(track['preview_url'], track['id'], data_folder)

    #Get 50 songs from user's library
    results = spotify.current_user_saved_tracks(limit=50)
    for item in results['items']:
        track = item['track']
        user_library[track['id']] = (track['name'], track['artists'])  # id = name, artist
        downloadMP3(track['preview_url'], track['id'], data_folder)

    return user_library

def make_playlist(name, ids):
    playlists = spotify.user_playlist_create(USERNAME, name, public=False)
    playlistID = playlists['id']
    spotify.user_playlist_add_tracks(USERNAME, playlistID, ids)
    return playlistID

if __name__ == '__main__':
    get_user_library("../library_data/")
