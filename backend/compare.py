import math
import numpy as np
from scipy.spatial.distance import cosine
from pprint import pprint

def dimensional_distance(query, song):
    query = np.array(query)
    song = np.array(song)
    idx = ~np.isnan(query) & ~np.isnan(song)
    query = query[idx]
    song = song[idx]
    return np.sqrt(np.average((query - song)**2))

def basic_distance(query_text, query_audio, song_text, song_audio):
    if query_text is None:
        if song_audio is not None:
            return np.max(np.abs(np.array(song_audio) - np.array(query_audio)))
        else:
            return 1
    if query_audio is None:
        if song_text is not None:
            return np.max(np.abs(np.array(song_text) - np.array(query_text)))
        else:
            return 1
    
    if song_audio is None:
        return np.max(np.abs(np.array(song_text) - np.array(query_text)))
    if song_text is None:
        return np.max(np.abs(np.array(song_audio) - np.array(query_audio)))
    return (np.max(np.abs(np.array(song_text) - np.array(query_text))) + np.max(np.abs(np.array(song_audio) - np.array(query_audio))))/2

def compare_dimensional(query_audio, query_text, library_audio, library_text, k = 15, include_query = True):
    query_ids = set(list(query_audio.keys()) + list(query_text.keys()))
    library_ids = set(list(library_audio.keys()) + list(library_text.keys()))
    assert len(query_ids) > 0, "empty query :("

    query_vec = [np.nan, np.nan, np.nan, np.nan]
    if len(query_text) > 0:
        query_vec[:2] = [sum([val["Arousal"] for val in query_text.values()])/len(query_text), sum([val["Valence"] for val in query_text.values()])/len(query_text)]
    if len(query_audio) > 0:
        query_vec[2:] = [sum([val["arousal"] for val in query_audio.values()])/len(query_audio), sum([val["valence"] for val in query_audio.values()])/len(query_audio)]

    distances = []
    for id in library_ids:
        song = [np.nan, np.nan, np.nan, np.nan]
        if id in library_text:
            song[:2] = [library_text[id]["Arousal"], library_text[id]["Valence"]]
        if id in library_audio:
            song[2:] = [library_audio[id]["arousal"], library_audio[id]["valence"]]
        distances.append((id, dimensional_distance(query_vec, song)))
    distances = sorted(distances, key = lambda d: d[1])
    # pprint(distances)

    if include_query:
        top_ids = [d[0] for d in distances[:k - len(query_ids)]] + list(query_ids)
    else:
        top_ids = [d[0] for d in distances[:k]]
    return top_ids

def compare_basic(query_audio, query_text, library_audio, library_text, k = 15, include_query = True):
    query_ids = set(list(query_audio.keys()) + list(query_text.keys()))
    library_ids = set(list(library_audio.keys()) + list(library_text.keys()))
    assert len(query_ids) > 0, "empty query :("

    query_text_prob = None
    query_audio_prob = None
    if len(query_text) > 0:
        query_text_prob = np.average([np.array(value) for value in query_text.values()])
    if len(query_audio) > 0:
        query_audio_prob = np.average([np.array(value) for value in query_audio.values()])

    distances = []
    for id in library_ids:
        if id not in library_text:
            score = basic_distance(query_text_prob, query_audio_prob, None, library_audio[id])
        elif id not in library_audio:
            score = basic_distance(query_text_prob, query_audio_prob, library_text[id], None)
        else:
            score = basic_distance(query_text_prob, query_audio_prob, library_text[id], library_audio[id])
        distances.append((id, score))
    
    distances = sorted(distances, key = lambda d: d[1])
    # pprint(distances)

    if include_query:
        top_ids = [d[0] for d in distances[:k - len(query_ids)]] + list(query_ids)
    else:
        top_ids = [d[0] for d in distances[:k]]
    return top_ids