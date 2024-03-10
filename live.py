import cv2
import face_recognition
import numpy as np
import pickle
from pathlib import Path

from gtts import gTTS
import pygame
import os
import tempfile
pygame.mixer.init()


def load_known_encodings(encodings_location):
    with open(encodings_location, 'rb') as f:
        known_encodings = pickle.load(f)
    return known_encodings['encodings'], known_encodings['names']

def speak_names(names):
    if len(names) == 1:
        text = f"{names[0]} is in front of you."
    elif len(names) == 2:
        text = f"{names[0]} and {names[1]} are in front of you."
    else:
        text = ", ".join(names[:-1]) + f", and {names[-1]} are in front of you."
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
        tts = gTTS(text)
        tts.write_to_fp(temp_audio)
    temp_audio_path = temp_audio.name
    pygame.mixer.music.load(temp_audio_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    os.remove(temp_audio_path)

known_face_encodings, known_face_names = load_known_encodings(Path("output/encodings.pkl"))

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
trigger_pressed = False

video_capture = cv2.VideoCapture(0)
distance_threshold = 0.35

while True:
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size - faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # BGR to RGB
    rgb_small_frame = np.array(small_frame[:, :, ::-1])
    
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "A stranger"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    
        if np.any(face_distances <= distance_threshold):
            
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
        else:
            name = "A stranger"

        face_names.append(name)


    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locs
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    key = cv2.waitKey(1)
    if key & 0xFF == ord(' '):
        trigger_pressed = True

    if trigger_pressed:
        sorted_face_names = [name for _, name in sorted(zip([left for _, _, _, left in face_locations], face_names))]
        speak_names(sorted_face_names)
        trigger_pressed = False

    # 'q' to quit
    if key & 0xFF == ord('q'):
        break
    
video_capture.release()
cv2.destroyAllWindows()
