from audio import *

with open('./static/audio_index.pkl', 'rb') as f:
    hashtable = pickle.load(f)

print search_audio('en.wav', hashtable)