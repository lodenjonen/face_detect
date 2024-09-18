import face_recognition
import os

# Path to the directory containing known face images
KNOWN_FACES_DIR = 'path/to/known_faces'  # Update this path to where your known faces are stored

def detect_faces(image_path):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    return face_encodings

def compare_with_database(face_encodings):
    known_face_encodings = []
    known_face_names = []

    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            image_path = os.path.join(KNOWN_FACES_DIR, filename)
            known_face_image = face_recognition.load_image_file(image_path)
            known_face_encoding = face_recognition.face_encodings(known_face_image)[0]
            known_face_encodings.append(known_face_encoding)
            known_face_names.append(filename)

    for encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, encoding)
        if True in matches:
            return True
    return False
