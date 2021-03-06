import os
import pickle
import numpy as np
import pandas as pd
import pydub
import json
from pprint import pprint

arousal_model = pickle.load(open("models/arousal_model.pkl", "rb"))
valence_model = pickle.load(open("models/valence_model.pkl", "rb"))
scaling = pd.read_csv("models/scaling.csv", index_col=0, header=0)
print("dimensional emotion model loaded")

if not os.path.exists("temp/"):
    os.makedirs("temp/")
    print("creating temp/")

def get_dimensional_emotion(ids, songs_folder = "data/", temp_folder = "temp/", limit = -1, remove_temp = False):
    song_ids = []
    
    for i, id in enumerate(ids): 
        found_features = False
        mp3_file_path = songs_folder + "{}.mp3".format(id)
        wav_file_path = temp_folder + "temp_{}.wav".format(id)
        feature_file_path = temp_folder + "temp_features_{}.csv".format(id)
        print("{}. id: {}...".format(i + 1, id), end = "")

        if not os.path.exists(feature_file_path):
            if os.path.exists(mp3_file_path):
                mp3_file = pydub.AudioSegment.from_mp3(mp3_file_path)
                mp3_file.export(wav_file_path, format="wav")
                print("converted mp3 to wav...", end = "")

                os.system("opensmile/inst/bin/SMILExtract -noconsoleoutput -C backend/IS13_ComParE_lld-func.conf -I {} -O {}".format(wav_file_path, feature_file_path))
                print("features created...", end = "")
                found_features = True
            else:
                print("mp3 not found...", end = "")
        else:
            found_features = True
            print("features already created...", end = "")

        if found_features:
            song_ids.append(id)
        print("done")

        if i == limit - 1:
            break

    if len(song_ids) == 0:
        return dict()

    columns = list(pd.read_csv("temp/temp_features_template.csv", delimiter = ";", index_col = 0, header = 0).columns)
    columns = [column for column in columns if column.endswith("_amean")]
    mean_columns = [column[:-6] + "_mean" for column in columns]
    std_columns = [column[:-6] + "_std" for column in columns]
    aggregate_df = pd.DataFrame(index = song_ids, columns = mean_columns + std_columns)

    for song_id in song_ids:
        feature_file_path = temp_folder + "temp_features_{}.csv".format(song_id)
        song_df = pd.read_csv(feature_file_path, delimiter = ";", index_col = 0, header = 0)
        aggregate_df.loc[song_id, mean_columns] = song_df[columns].mean().values.copy()
        aggregate_df.loc[song_id, std_columns] = song_df[columns].std().values.copy()
    print("features aggregated for songs")

    if remove_temp:
        print("removing temp wav and feature files...", end = "")
        for song_id in song_ids:
            wav_file_path = temp_folder + "temp_{}.wav".format(song_id)
            feature_file_path = temp_folder + "temp_features_{}.csv".format(song_id)
            os.system("rm {} {}".format(wav_file_path, feature_file_path))
        print("done\n")

    emotion_df = pd.DataFrame(index = song_ids, columns = ["arousal","valence"])
    aggregate_df_scaled = (aggregate_df - scaling["mean"])/scaling["std"]
    emotion_df["arousal"] = (arousal_model.predict(aggregate_df_scaled) - 1)/8
    emotion_df["valence"] = (valence_model.predict(aggregate_df_scaled) - 1)/8
    print("dimensional audio emotion calculated\n")

    return emotion_df.transpose().to_dict()

if __name__ == "__main__":
    dictionary = json.load(open("dictionary.json"))
    dimensional_dict = get_dimensional_emotion(dictionary)
    pprint(dimensional_dict)