from .spotify import search, get_user_library, make_playlist
from .lyrics import download_lyrics
from .text_emotion import get_basic_text_emotion, get_dimensional_text_emotion
from .dimensional_emotion import get_dimensional_emotion
from .basic_emotion import get_basic_emotion
from .compare import compare_basic, compare_dimensional
import pickle
from pprint import pprint

def backend(user_query, k = 15):
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

    print("comparing average query and user library...")
    avg_basic_ids = compare_basic(query_basic_audio_emotion, query_basic_text_emotion, library_basic_audio_emotion, library_basic_text_emotion, k)
    avg_dimensional_ids = compare_dimensional(query_dimensional_audio_emotion, query_dimensional_text_emotion, library_dimensional_audio_emotion, library_dimensional_text_emotion, k)

    print("comparing each query and user library...")
    var_basic_ids = []
    var_dimensional_ids = []
    query_ids = list(query.keys())
    for q_id in query_ids:
        if q_id in query_basic_audio_emotion:
            single_query_basic_audio_emotion = {q_id: query_basic_audio_emotion[q_id]}
        else:
            single_query_basic_audio_emotion = {}
        if q_id in query_basic_text_emotion:
            single_query_basic_text_emotion = {q_id: query_basic_text_emotion[q_id]}
        else:
            single_query_basic_text_emotion = {}
        if q_id in query_dimensional_audio_emotion:
            single_query_dimensional_audio_emotion = {q_id: query_dimensional_audio_emotion[q_id]}
        else:
            single_query_dimensional_audio_emotion = {}
        if q_id in query_dimensional_text_emotion:
            single_query_dimensional_text_emotion = {q_id: query_dimensional_text_emotion[q_id]}
        else:
            single_query_dimensional_text_emotion = {}

        var_basic_ids.extend(compare_basic(single_query_basic_audio_emotion, single_query_basic_text_emotion, library_basic_audio_emotion, library_basic_text_emotion, k//len(query), include_query=False))
        var_dimensional_ids.extend(compare_dimensional(single_query_dimensional_audio_emotion, single_query_dimensional_text_emotion, library_dimensional_audio_emotion, library_dimensional_text_emotion, k//len(query), include_query=False))
    var_basic_ids = list(set(var_basic_ids)) + query_ids
    var_dimensional_ids = list(set(var_dimensional_ids)) + query_ids

    pickle.dump(avg_basic_ids, open("avg_basic_ids.pkl","wb"))
    pickle.dump(avg_dimensional_ids, open("avg_dimen_ids.pkl","wb"))
    pickle.dump(var_basic_ids, open("var_basic_ids.pkl","wb"))
    pickle.dump(var_dimensional_ids, open("var_dimen_ids.pkl","wb"))

    print("making playlists")
    make_playlist("Basic Playlist Avg", avg_basic_ids)
    make_playlist("Dimen Playlist Avg", avg_dimensional_ids)
    make_playlist("Basic Playlist Var", var_basic_ids)
    make_playlist("Dimen Playlist Var", var_dimensional_ids)

if __name__ == "__main__":
    # test_query = [("Quiet things","Brand new"),("I'm not okay","My Chemical Romance"),("Have faith in me","Day to remember")]
    test_query = [("Stuntman", "Danakadan"), ("Murals", "Dumbfoundead"), ("Ridin through LA", "D pryde")]
    backend(test_query)