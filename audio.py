# -*- coding:utf-8 -*-
from scipy.io import wavfile
from scipy.ndimage import maximum_filter
import librosa
import numpy as np
import os
import pickle
import sys

def load_wavfile(path):
    """读取wav文件"""
    sr, wav = wavfile.read(path)
    bits = wav.itemsize * 8
    wav = wav/(2 ** (bits - 1))  # 将int转化为float，即压缩到[0, 1)
    if wav.ndim == 2:
        wav = np.mean(wav, axis=-1)  # 双声道转化为单声道
    return wav


def get_peaks(y, threshold=10):
    """找出y中的峰值点坐标
    y: 2D array.
    threshold: 过滤幅值过小的峰值点的阈值
    Returns: List containing (freq_id, time_id)."""
    maximum = maximum_filter(y, size=10) == y
    freq_id, time_id = np.nonzero(maximum)
    amps = y[maximum].reshape(-1)
    peaks = zip(freq_id, time_id, amps)
    peaks = [(x[0], x[1]) for x in peaks if x[2] > threshold]
    return peaks


def get_features(peaks):
    features = []
    for i in range(len(peaks)):
        for j in range(1, 6):
            if i + j < len(peaks):
                freq1 = peaks[i][0]
                freq2 = peaks[i + j][0]
                t1 = peaks[i][1]
                t2 = peaks[i + j][1]
                t_delta = t2 - t1

                if t_delta >= 0 and t_delta <= 200:
                    h = (freq1, freq2, t_delta)
                    features.append((h, t1))
    return features


def get_fingerprints(wav):
    """从wav数据中提取特征"""
    spec = np.abs(librosa.stft(wav))
    peaks = get_peaks(spec)
    return get_features(peaks)


def create_index(dir_path):
    """预处理数据库中的数据，创建索引并保存在文件中
    dir: 存放音乐数据的文件夹路径，里面放置wav文件
    """
    filenames = os.listdir(dir_path)
    i = 1
    hashtable = {}
    for filename in filenames:
        filepath = os.path.join(dir_path, filename)
        print "processing {} {}".format(i, filename)
        i += 1
        wav = load_wavfile(filepath)
        fps = get_fingerprints(wav)
        for fp in fps:
            t = fp[1]
            fp = fp[0]
            if fp not in hashtable:
                hashtable[fp] = [(filename, t)]
            else:
                hashtable[fp].append((filename, t))

    with open('./static/audio_index.pkl', 'wb') as f:
        pickle.dump(hashtable, f)


def search_audio(path, hashtable):
    """搜索目标文件，返回5条（歌曲，时间差）的最佳匹配"""
    wav = load_wavfile(path)
    fingerprints = get_fingerprints(wav)
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


if __name__ == '__main__':
    dir_path = sys.argv[1]
    create_index(dir_path)


