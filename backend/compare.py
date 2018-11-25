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

# def basic_distance(query, song):

def compare_dimensional(query_audio, query_text, library_audio, library_text, k = 15):
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
    pprint(distances)

    top_ids = [d[0] for d in distances[:k - len(query_ids)]] + list(query_ids)
    return top_ids

def compare_basic(query_audio, query_text, library_audio, library_text, k = 15):
    query_text_avg = np.average([np.array(value) for value in query_text.values()])
    query_audio_avg = np.average([np.array(value) for value in query_audio.values()])

    scores = []
    ids = set(list(library_audio.keys()) + list(library_text.keys()))
    query_ids = list(set(list(query_audio.keys()) + list(query_text.keys())))
    for id in ids:
        text_score = 0
        audio_score = 0
        if id in library_text:
            text_score = cosine(library_text[id], query_text_avg)
        if id in library_audio:
            audio_score = cosine(library_audio[id], query_audio_avg)
        scores.append({"id": id, "text_score": text_score, "audio_score": audio_score, "total_score": text_score + audio_score})
    scores = sorted(scores, key = lambda s: s["total_score"], reverse = True)
    
    top_ids = [v["id"] for v in scores[:k]]
    top_ids.extend(query_ids)
    return list(set(top_ids))