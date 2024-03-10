import cv2
import os

name = 'Dyllan'

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
    elif k%256 == 32:
        # SPACE pressed
        img_name = "{}/{}_{}.jpg".format(dataset_dir, name, img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()
cv2.destroyAllWindows()
