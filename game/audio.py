class audio:
	import RPI.GPIO as GPIO
	import time

	def __init__(self):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(0, GPIO.OUT)	#pin 0 for data selector, bit 0
		GPIO.setup(1, GPIO.OUT)	#pin 1 for data selector, bit 1
		GPIO.setup(2, GPIO.OUT)	#pin 2 for PWM audio

	#A function to enable one of three audio channels, for internal use only
	#Line: 0 for off, 1 for osc1, 2 for osc2, 3 for gpio PWM
	#Delay: length of time the channel is enabled in seconds
	def __enable_audio_line(self, line, delay):
		if(line == 1):
			GPIO.output(0, True)
			time.sleep(delay)
			GPIO.output(0, False)
		if(line == 2):
			GPIO.output(1, True)
			time.sleep(delay)
			GPIO.output(1, False)
		if(line == 3):
			GPIO.output(0, True)
			GPIO.output(1, True)
			time.sleep(delay)
			GPIO.output(0, False)
			GPIO.output(1, False)

	#a function to sound the tone generated by osc1 for a given delay
	def tone1(self, delay):
		try:
			thread.start_new_thread(self.__enable_audio_line(1, delay), ())
		except:
			print('Unable to play tone, could not open thread')

	#a function to sound the tone generated by osc2 for a given delay
	def tone2(self, delay):
		try:
			thread.start_new_thread(self.__enable_audio_line(2, delay), ())
		except:
			print('Unable to play tone, probably unable to open thread')

	def intro_music(self):
		try:
			thread.start_new_thread(self.__play_intro_music(), ())
		except:
			print('Unable to play intro music, unable to open thread')

	#outputs a single tone to GPIO pin 3 using PWM, for internal use only
	#period: period of each pulse in the tone
	#mark & space: sets the mark-space ratio - should add to 1
	#delay: the length of time that the tone should sound for, in seconds
	def __play_tone(self, period, mark, space, delay):
		if(not(mark + space == 1)):
			raise ValueError('Invalid mark-space ratio')

		while(delay > 0):
			GPIO.output(2, True)
			time.sleep(period*mark)
			GPIO.output(2, False)
			time.sleep(period*space)
			delay -= period

	#plays the intro music, for internal use only
	#delay of 0.4 = crotchet
	def __play_intro_music(self):
		GPIO.output(0, True)
		GPIO.output(1, True)
		self.__play_tone(self, 1/440, 0.5, 0.5, 0.4)	#Play A crotchet
		self.__play_tone(self, 1/466.16, 0.5, 0.5, 0.2)	#Play A# quaver	
		self.__play_tone(self, 1/493.88, 0.5, 0.5, 0.4)	#Play B crotchet
		self.__play_tone(self, 1/440, 0.5, 0.5, 0.2)	#Play A quaver	
		self.__play_tone(self, 0, 0.5, 0.5, 0.2)	#Rest quaver	
		self.__play_tone(self, 1/554.37, 0.5, 0.5, 0.2)	#Play C# quaver
		self.__play_tone(self, 1/554.37, 0.5, 0.5, 0.2)	#Play C# quaver
		self.__play_tone(self, 0, 0.5, 0.5, 0.2)	#Rest quaver
		self.__play_tone(self, 1/554.37, 0.5, 0.5, 0.2)	#Play C# quaver
		self.__play_tone(self, 1/554.37, 0.5, 0.5, 0.2)	#Play C# quaver
		GPIO.output(0, False)
		GPIO.output(1, False)


