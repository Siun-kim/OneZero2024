import cv2
import os
import subprocess
import speech_recognition as sr
import sounddevice as sd
import numpy as np
from playsound import playsound
from gtts import gTTS
import tempfile
import pygame
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

button_pressed = False
def button_callback(channel):
    global button_pressed
    button_pressed = True

pygame.mixer.init()
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge


fps = 44100
duration = 3

def speak(text):
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
        tts = gTTS(text)
        tts.write_to_fp(temp_audio)
    temp_audio_path = temp_audio.name
    #playsound(temp_audio_path)
    pygame.mixer.music.load(temp_audio_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    os.remove(temp_audio_path)

'''
def verify_name(name):
    speak(f"Is the name {name} correct? Please answer in yes or no.")
    print("Verifying name...")

    verification_duration = 3  
    verification_recording = sd.rec(verification_duration * fps, samplerate=fps, channels=1, dtype='int16')
    sd.wait()

    verification_rec = sr.Recognizer()
    verification_audio_data = np.squeeze(verification_recording)
    verification_audio_data = sr.AudioData(
        verification_audio_data.tobytes(),
        sample_rate=fps,
        sample_width=2
    )

    try:
        response = verification_rec.recognize_google(verification_audio_data)
        print("Response recognized:", response)
        return response.lower() == "yes"
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        speak("Sorry, I didn't catch that. Please answer in yes or no.")
        return False
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service:", e)
        speak("Sorry, there was an error. Please try again.")
        return False

def get_name():

    speak("What is the name of the person you want to add?")
    print("Listening for name...")

    recording = sd.rec(duration * fps, samplerate=fps, channels=1, dtype='int16')
    sd.wait()

    rec = sr.Recognizer()
    audio_data = np.squeeze(recording)
    audio_data = sr.AudioData(
        audio_data.tobytes(),
        sample_rate=fps,
        sample_width=2
    )

    try:
        name = rec.recognize_google(audio_data)
        print("Name recognized:", name)
        return name
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        speak("Sorry, I didn't catch that. Please try again.")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service:", e)
        speak("Sorry, there was an error. Please try again.")
        return None
'''
# Main code
name = input("Enter name of the person: ")

'''
while not name:
    name = get_name()
    if name:
        if not verify_name(name):
            name = None
'''
if name:
    speak(f"Ready to take pictures of {name}.")

dataset_dir = "train/" + name
os.makedirs(dataset_dir, exist_ok=True)

cam = cv2.VideoCapture(0)

cv2.namedWindow("press space to take a photo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("press space to take a photo", 500, 300)

img_counter = 0
existing_files = os.listdir(dataset_dir)
for filename in existing_files:
    if filename.startswith(name):
        img_counter = max(img_counter, int(filename.split('_')[-1].split('.')[0]))

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("press space to take a photo", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Exciting...")
        break
    elif k%256 == 32 or button_pressed == True:
        # SPACE or button pressed
        button_pressed = False
        img_name = "{}/{}_{}.jpg".format(dataset_dir, name, img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()
cv2.destroyAllWindows()

subprocess.run(["python", "encode.py"])
