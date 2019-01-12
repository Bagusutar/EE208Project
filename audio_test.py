from audio import *

with open('Index.pkl', 'rb') as f:
    hashtable = pickle.load(f)

a = load_wavfile('en.wav')
print search(a)