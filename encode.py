import pickle
from pathlib import Path

import face_recognition

DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")

# Load existing encodings
existing_encodings = {}
if DEFAULT_ENCODINGS_PATH.exists():
    with DEFAULT_ENCODINGS_PATH.open(mode="rb") as f:
        existing_encodings = pickle.load(f)

names = existing_encodings.get("names", [])
encodings = existing_encodings.get("encodings", [])

existing_names = set(names)

for filepath in Path("train").glob("*/*"):
    if not filepath.suffix.lower() in ['.jpg', '.jpeg', '.png']:
        continue
    name = filepath.parent.name
    # Skip already encoded ones
    if name in existing_names:
        continue
    image = face_recognition.load_image_file(filepath)

    face_locations = face_recognition.face_locations(image, model="hog")
    face_encodings = face_recognition.face_encodings(image, face_locations)

    for encoding in face_encodings:
        names.append(name)
        encodings.append(encoding)

name_encodings = {"names": names, "encodings": encodings}
with DEFAULT_ENCODINGS_PATH.open(mode="wb") as f:
    pickle.dump(name_encodings, f)



