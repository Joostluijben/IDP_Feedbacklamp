import pyaudio
import audioop
import numpy as np
import time
# initialise pyaudio get channels and rate automaticly, also set chunk size
pa = pyaudio.PyAudio()
CHUNK = 16
RATE = int(pa.get_device_info_by_index(2).get('defaultSampleRate'))
CHANNELS = int(pa.get_device_info_by_index(2).get('maxInputChannels'))
stream = pa.open(format = pyaudio.paInt16,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    frames_per_buffer = 16,
    input_device_index=2)
def readAudio():
    audioLst = []
    # calculate the root mean square of every chunk and put it in a list. Return the average of this list
    for i in range(1000):
        data = stream.read(CHUNK, exception_on_overflow=False)
        rms = audioop.rms(data,2)
        audioLst.append((20*np.log(rms)))
    found = sum(audioLst)/len(audioLst)
    return found
