# Recogneyes

Recogneyes addresses the challenges faced by visually impaired individuals when trying to recognize faces. It aims to support individuals facing challenges in social interactions or name recall by enhancing memory recall and helping maintain meaningful connections.

This project was made in under 24 hours as part of Cornell's 2024 BigRed//Makeathon and won 2nd Best Overall.

Check out our slides: [link](https://github.com/anniesiun/OneZero2024/blob/main/Sp2024%20Hackathon%20-%20RecognEyes.pdf) 

## Purpose

The purpose of Recogneyes is to:

- Empower visually impaired individuals to navigate social situations confidently.
- Aid in name memory retention and recall.
- Enhance independence and enrich daily interactions for its users.

## Technology

### Software

Recogneyes employs computer vision algorithms to conduct real-time facial recognition. It also generates auditory feedback using speech-to-text and text-to-speech technology.

### Hardware

The glasses are powered by a Raspberry Pi 4 microcontroller connected with a Pi camera.

## Figma Prototype

This is an app prototype that serves as a companion to the Recogneyes glasses. Users can configure their profiles, add friends and family to their network, and utilize additional features.

[Figma Prototype Link](https://www.figma.com/file/VgBGpJm6Vs8xozuynFibVS/Makeathon-Project?type=design&node-id=48%3A2217&mode=design&t=BxCQrCPd6oUqANeg-1)

## How to Use

1. Clone the repository to your local machine

2. Navigate to the project directory

3. Install any dependencies required

4. Run the `takePhoto.py` script. It will prompt you audibly to speak the name of the person you want to add and confirm afterward. Tip: Wait one second after the computer ends their speech before speaking.

5. Then, when the computer says "Ready to take pictures of [name]" and the camera pops out, all you have to do is press the space bar and it will take the pictures. It doesn't matter how many, but the more you enter into the dataset, the better the model. However, about 10 works just fine. Also tip: when taking the pictures, tell whoever you are taking a picture of to have various facial expressions and also take the photos at a wide variety of angles to improve performance. When finished, press quit. 

6. The model automatically starts training on the images you have just taken, so give it a minute.

7. After training, running `live.py` will open the camera and start recognizing faces. If you press the space bar, it will speak out loud who it has recognized from left to right.
