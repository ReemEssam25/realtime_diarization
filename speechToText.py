####################################
# to install packages
# pip3 install SpeechRecognition pydub
# for mic #
# pip install wheel
# pip install pipwin
# pipwin install pyaudio

import speech_recognition as sr

'''

filename = "X2zqiX6yL3I.wav"
r = sr.Recognizer()

with sr.AudioFile(filename) as source:
    # listen for the data (load audio to memory)
    audio_data = r.record(source)
    # recognize (convert from speech to text)
    text = r.recognize_google(audio_data, language="ar-EG")
    print(text)
'''

r = sr.Recognizer()
#file_object = open('test.txt','w')
while (True):
    with sr.Microphone() as source:
        # read the audio data from the default microphone
        audio_data = r.record(source, duration=5)
        print("Recognizing...")
        # convert speech to text
        try:
            text = r.recognize_google(audio_data, language="ar-EG")
            #file_object.write(text)
            print(text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
