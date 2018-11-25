import pandas as pd

def read_basic_emotion_lexion():
    emotion_dict = dict()
    with open("text/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt") as f:
        for i, line in enumerate(f):
            if i >= 46:
                word, emotion, sentiment = line.strip().split('\t')
                if int(sentiment) == 1:
                    if word not in emotion_dict:
                        emotion_dict[word] = []
                    emotion_dict[word].append(emotion)
    return emotion_dict

def read_dimensional_emotion_lexicon(): 
    data = pd.read_csv("text/NRC-VAD-Lexicon.txt", delimiter = "\t")
    return data