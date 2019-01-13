from audio import *

with open('./static/audio_index.pkl', 'rb') as f:
    hashtable = pickle.load(f)

print 'the results of en.wav'
print search_audio('test/en.wav', hashtable)