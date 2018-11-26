import os
import lyricsgenius as genius
from PyLyrics import PyLyrics

genius_api = genius.Genius("9mXsJ6OfC-KdM2QF1xl_0hRVZ7KiqrQYtUwobdB4kcpVsClOHUGf_d1a8qQjfIoa", verbose=False)

def download_from_pylyrics(track, artist):
    try:
        text = PyLyrics.getLyrics(artist, track)
        return text
    except:
        return None

def download_from_genius(track, artist):
    song = genius_api.search_song(track, artist)
    if song is not None:
        text = song.lyrics
        return text
    return None

def download(track, artist):
    text = download_from_genius(track, artist)
    if text is None:
        return download_from_pylyrics(track, artist)
    else:
        return text

def download_lyrics(data, data_folder):
    for i, (id, (track, artists_info)) in enumerate(data.items()):
        if os.path.exists("{}{}_lyrics.txt".format(data_folder, id)):
            print("{}. id: {} lyrics already found :)".format(i + 1, id))
            continue

        for punctuation in ["-","!","?","("]:
            idx = track.find(punctuation)
            if idx != -1:
                track = track[:idx].strip()
        artists = [artist_info["name"] for artist_info in artists_info]
        artist_joined = ' & '.join(artists)

        possible_tracks = [track]
        possible_artists = [artists[0], artist_joined]
        if len(artists) >= 2:
            artist_joined_2 = " & ".join(artists[:2])
            possible_artists.append(artist_joined_2)

        possible_combinations = [(track, artist) for track in possible_tracks for artist in possible_artists]
        text = None
        for combination in possible_combinations:
            text = download(*combination)
            if text is not None:
                break
        if text is not None:
            print("{}. id: {} lyrics found :)".format(i+1,id))
            with open("{}{}_lyrics.txt".format(data_folder, id),"w") as fout:
                fout.write(text)
        else:
            print("{}. id: {} lyrics not found :(".format(i+1,id))
    print()