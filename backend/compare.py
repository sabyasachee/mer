import math
import numpy as np
from scipy.spatial.distance import cosine
from pprint import pprint

def compare_dimensional(query_audio, query_text, library_audio, library_text, k = 15):
    query_text_arousal = sum([value["Arousal"] for value in query_text.values()])/len(query_text)
    query_text_valence = sum([value["Valence"] for value in query_text.values()])/len(query_text)
    query_audio_arousal = sum([value["arousal"] for value in query_audio.values()])/len(query_audio)
    query_audio_valence = sum([value["valence"] for value in query_audio.values()])/len(query_audio)

    scores = []
    ids = set(list(library_audio.keys()) + list(library_text.keys()))
    query_ids = list(set(list(query_audio.keys()) + list(query_text.keys())))
    for id in ids:
        text_score = 0
        audio_score = 0
        if id in library_text:
            text_arousal = library_text[id]["Arousal"]
            text_valence = library_text[id]["Valence"]
            text_score = math.sqrt((text_arousal - query_text_arousal)**2 + (text_valence - query_text_valence)**2)
        if id in library_audio:
            audio_arousal = library_audio[id]["arousal"]
            audio_valence = library_audio[id]["valence"]
            audio_score = math.sqrt((audio_arousal - query_audio_arousal)**2 + (audio_valence - query_audio_valence)**2)
        scores.append({"id": id, "text_score": text_score, "audio_score": audio_score, "total_score": text_score + audio_score})
    scores = sorted(scores, key = lambda s: s["total_score"], reverse=True)
    
    top_ids = [v["id"] for v in scores[:k]]
    top_ids.extend(query_ids)
    return list(set(top_ids))

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