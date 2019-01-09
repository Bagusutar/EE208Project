from scipy.io import wavfile
import librosa
import numpy as np
import os
import pickle
import hashlib
from scipy.fftpack import fft
from scipy.ndimage import maximum_filter


def load_wavfile(path):
    sr, wav = wavfile.read(path)
    bits = wav.itemsize * 8
    wav = wav/(2 ** (bits - 1))
    if wav.ndim == 2:
        wav = np.mean(wav, axis=-1)
    return wav


def get_peaks(y):
    """Input: 2D array.
       Output: 2D boolean array with the same shape."""
    maximum = maximum_filter(y, size=10) == y
    freq_id, time_id = np.nonzero(maximum)
    amps = y[maximum].reshape(-1)
    peaks = zip(freq_id, time_id, amps)
    peaks = [x for x in peaks if x[2] > 10]
    return peaks


def get_hashes(peaks):
    hashes = []
    for i in range(len(peaks)):
        for j in range(1, 16):
            if i + j < len(peaks):
                freq1 = peaks[i][0]
                freq2 = peaks[i + j][0]
                t1 = peaks[i][1]
                t2 = peaks[i + j][1]
                t_delta = t2 - t1

                if t_delta >= 0 and t_delta <= 200:
                    h = (freq1, freq2, t_delta)
                    hashes.append((h, t1))
    return hashes


def fingerprints(wav):
    spec = np.abs(librosa.stft(wav))
    peaks = get_peaks(spec)
    return get_hashes(peaks)


def create_index():
    path = "C:\\Users\\ihone\\OneDrive\\桌面\\111"
    filenames = os.listdir(path)
    i=1
    hashtable = {}
    for filename in filenames:
        filepath = os.path.join(path, filename)
        print(i,filename)
        i+=1
        wav = load_wavfile(filepath)
        fps = fingerprints(wav)
        for fp in fps:
            t = fp[1]
            fp = fp[0]
            if fp not in hashtable:
                hashtable[fp] = [(filename, t)]
            else:
                hashtable[fp].append((filename, t))

    with open('Index.pkl', 'wb') as f:
        pickle.dump(hashtable, f)


def search(fingerprints, hashtable):
    res = {}
    for fp in fingerprints:
        t = fp[1]
        fp = fp[0]
        for dst in hashtable.get(fp, []):
            name = dst[0]
            time = dst[1]
            delta_t = t - time
            idx = (name, delta_t)
            if idx in res:
                res[idx] += 1
            else:
                res[idx] = 1
    return sorted(res.items(), key=lambda x: x[1], reverse=True)[:5]


a = load_wavfile('Deja Vu.wav')
df = fingerprints(a)
aa = load_wavfile('ha.wav')
ff = fingerprints(aa)
aaa = load_wavfile('1 (1).wav')
fff = fingerprints(aaa)
print(len(df))
print(len(ff))
print(len(fff))

# create_index()
with open('Index.pkl', 'rb') as f:
    hashtable = pickle.load(f)
for fp in df:
    t=fp[1]
    fp=fp[0]
    if fp not in hashtable:
        hashtable[fp] = [('djv',t)]
    else:
        hashtable[fp].append(('djv',t))

print(search(fff, hashtable))
print(search(ff,hashtable))
aaaa = load_wavfile('subdjv.wav')
ffff= fingerprints(aaaa)
print(search(ffff,hashtable))