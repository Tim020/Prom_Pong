from game.audio import *
import time

while True:
	audio = Audio()
	audio.tone1(4)
	time.sleep(5)
	audio.tone2(4)
	time.sleep(5)
	audio.intro_music()
