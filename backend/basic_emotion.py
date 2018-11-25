import os
import librosa
import numpy as np
from scipy import signal
import torch
from .conv_net import ConvNet

angry_model = ConvNet(1)
angry_model.load_state_dict(torch.load('models/angry_model.pth'))
angry_model.eval()

fear_model = ConvNet(1)
fear_model.load_state_dict(torch.load('models/fear_model.pth'))
fear_model.eval()

happy_model = ConvNet(1)
happy_model.load_state_dict(torch.load('models/happy_model.pth'))
happy_model.eval()

sad_model = ConvNet(1)
sad_model.load_state_dict(torch.load('models/sad_model.pth'))
sad_model.eval()
print("basic emotion models loaded")

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
            angry_pred = angry_model(spec)
            angry_pred = angry_pred.data.numpy()
            angry_pred = list(angry_pred[0])
            fear_pred = fear_model(spec)
            fear_pred = fear_pred.data.numpy()
            fear_pred = list(fear_pred[0])
            happy_pred = happy_model(spec)
            happy_pred = happy_pred.data.numpy()
            happy_pred = list(happy_pred[0])
            sad_pred = sad_model(spec)
            sad_pred = sad_pred.data.numpy()
            sad_pred = list(sad_pred[0])
            
            final_pred = np.array(angry_pred + fear_pred + happy_pred + sad_pred)
            
            songs_emo[id] = final_pred
            print("basic emotion calculated")
        else:
            print("mp3 file not found")
    print()
    return songs_emo
