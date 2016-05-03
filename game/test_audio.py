from audio import *
import time

audio = Audio()

while True:	
    print "playing tone1"
    #audio.tone1(1)
    print "playing tone2"
    #audio.tone2(1)
    print "playing intro music"
    audio.intro_music()
    print "resting"
    time.sleep(1)
