import os
import librosa
import numpy as np
from scipy import signal
import torch
from .conv_net import ConvNet

model = ConvNet(6)
model.load_state_dict(torch.load('models/model.pth'))
model.eval()
print("basic emotion model loaded")

def audio_read(f):
    y, _ = librosa.core.load(f, sr=None)
    nfft = 512
    nperseg = 512
    M = nfft/2 + 1
    noverlap = ((M+1)*nperseg - len(y))/M
    _, _, Zxx = signal.spectrogram(y, window='hamming', nperseg=nperseg, noverlap=noverlap, nfft=nfft, mode='complex')
    Zxx = Zxx[:,0:257]
    S = np.abs(10*Zxx)**2
    return S

def get_basic_emotion(ids, songs_folder = "data/"):
    songs_emo = {}
    for i, id in enumerate(ids):
        print("{}. id: {} ...".format(i + 1, id), end = "")
        mp3_file_path = "{}{}.mp3".format(songs_folder, id)
        if os.path.exists(mp3_file_path):
            spec = audio_read(mp3_file_path)# extract spectrogram 
            spec = np.expand_dims(spec, axis=0)
            spec = np.expand_dims(spec, axis=0)
            spec = torch.from_numpy(spec)
            pred = model(spec)
            pred = pred.data.numpy()
            pred = pred[0]
            pred = np.array(pred)
            songs_emo[id] = pred
            print("basic emotion calculated")
        else:
            print("mp3 file not found")
    print()
    return songs_emo