import os
from utils import read_basic_emotion_lexion, read_dimensional_emotion_lexicon

dimensional_emotion_lexicon = read_dimensional_emotion_lexicon()
basic_emotion_lexicon = read_basic_emotion_lexion()
dimensional_emotions = list(dimensional_emotion_lexicon)[1:]
basic_emotions = {x for y in basic_emotion_lexicon.values() for x in y}
print("text emotion lexicons loaded")

def get_basic_text_emotion(ids, data_folder):
    basic_text_emotion = {}
    for i, id in enumerate(ids):
        print("{}. id: {}...".format(i + 1, id), end = "")
        lyrics_file_path = "{}{}_lyrics.txt".format(data_folder, id)
        if os.path.exists(lyrics_file_path):
            with open(lyrics_file_path) as fin:
                text = fin.read()

                emotion_count = dict()
                for emotion in basic_emotions:
                    emotion_count[emotion] = 0

                n_words = 0
                for word in text.split():
                    if word in basic_emotion_lexicon:
                        n_words += 1
                        for e in basic_emotion_lexicon[word]:
                            emotion_count[e] += 1
                if n_words > 0:    
                    for e in basic_emotions:
                        emotion_count[e] = emotion_count[e]/n_words
                
                total = emotion_count['anger']+emotion_count['disgust']+emotion_count['fear']+emotion_count['joy']+emotion_count['sadness']+emotion_count['anticipation']
                if total > 0:
                    vector = [emotion_count['anger']/total, emotion_count['anticipation']/total, emotion_count['disgust']/total, emotion_count['fear']/total, emotion_count['joy']/total, emotion_count['sadness']/total]
                else:
                    vector = [0,0,0,0,0,0]
                basic_text_emotion[id] = vector
                print("basic emotion text calculated")
        else:
            print("lyrics not found")
    print()
    return basic_text_emotion

def get_dimensional_text_emotion(ids, data_folder):
    dimensional_text_emotion = {}
    for i, id in enumerate(ids):
        print("{}. id: {}...".format(i + 1, id), end = "")
        lyrics_file_path = "{}{}_lyrics.txt".format(data_folder, id)
        if os.path.exists(lyrics_file_path):
            with open(lyrics_file_path) as fin:
                text = fin.read()

                emotion_count = dict()
                for e in dimensional_emotions:
                    emotion_count[e] = 0
                n_words = 0
                for word in text.split():
                    row = dimensional_emotion_lexicon.loc[dimensional_emotion_lexicon['Word'] == word]
                    if not row.empty:
                        n_words += 1
                        for e in dimensional_emotions:
                            emotion_count[e] += row[e].iloc[0]
                if n_words > 0:
                    for e in dimensional_emotions:
                        emotion_count[e] = emotion_count[e]/n_words

                dimensional_text_emotion[id] = emotion_count
                print("dimensional emotion text calculated")
        else:
            print("lyrics not found")
    print()
    return dimensional_text_emotion