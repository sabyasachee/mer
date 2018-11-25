from .spotify import search, get_user_library, make_playlist
from .lyrics import download_lyrics
from .text_emotion import get_basic_text_emotion, get_dimensional_text_emotion
from .dimensional_emotion import get_dimensional_emotion
from .basic_emotion import get_basic_emotion
from .compare import compare_basic, compare_dimensional
from pprint import pprint

def backend(user_query):
    print("processing query...")
    query = search(user_query, "query_data/")
    download_lyrics(query, "query_data/")
    query_basic_text_emotion = get_basic_text_emotion(query.keys(), "query_data/")
    query_dimensional_text_emotion = get_dimensional_text_emotion(query.keys(), "query_data/")
    query_dimensional_audio_emotion = get_dimensional_emotion(query.keys(), songs_folder="query_data/", temp_folder="temp/")
    query_basic_audio_emotion = get_basic_emotion(query.keys(), songs_folder="query_data/")

    print("processing user library...")
    user_library = get_user_library("library_data/")
    download_lyrics(user_library, "library_data/")
    library_basic_text_emotion = get_basic_text_emotion(user_library.keys(), "library_data/")
    library_dimensional_text_emotion = get_dimensional_text_emotion(user_library.keys(), "library_data/")
    library_dimensional_audio_emotion = get_dimensional_emotion(user_library.keys(), songs_folder="library_data/", temp_folder="temp/")
    library_basic_audio_emotion = get_basic_emotion(user_library.keys(), songs_folder="library_data/")

    print("comparing query and user library...")
    basic_ids = compare_basic(query_basic_audio_emotion, query_basic_text_emotion, library_basic_audio_emotion, library_basic_text_emotion)
    dimensional_ids = compare_dimensional(query_dimensional_audio_emotion, query_dimensional_text_emotion, library_dimensional_audio_emotion, library_dimensional_text_emotion)

    print("making playlists")
    # make_playlist("Basic Playlist", basic_ids)
    # make_playlist("Valence Arousal Playlist", dimensional_ids)

if __name__ == "__main__":
    test_query = [("Happy","Williams"),("Hello","Adele"),("We are the champions","Queen")]
    backend(test_query)