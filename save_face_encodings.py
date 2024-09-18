# save_face_encodings.py

import face_recognition
import pickle
import cv2

def save_face_encodings(image_path, encodings_file):
    # Load image
    image = face_recognition.load_image_file(image_path)
    
    # Get face encodings
    encodings = face_recognition.face_encodings(image)
    
    if not encodings:
        raise ValueError("No faces found in the image.")
    
    # Save encodings to file
    with open(encodings_file, 'wb') as f:
        pickle.dump(encodings, f)

if __name__ == "__main__":
    save_face_encodings('/home/tatsuhirosatou/Desktop/hackathon/face_detection_project/static/person2.jpeg', 'static/face_encodings.pkl')
