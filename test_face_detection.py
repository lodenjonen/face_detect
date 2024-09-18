import face_recognition

def test_face_detection():
    # Path to the known face image
    known_face_path = '/home/tatsuhirosatou/Desktop/hackathon/face_detection_project/static/person2.jpeg'
    
    # Load the known face
    known_image = face_recognition.load_image_file(known_face_path)
    known_face_encoding = face_recognition.face_encodings(known_image)[0]

    # Test with the same known face image
    test_image = face_recognition.load_image_file(known_face_path)
    test_face_encoding = face_recognition.face_encodings(test_image)[0]

    # Compare the test face with the known face
    results = face_recognition.compare_faces([known_face_encoding], test_face_encoding)
    
    print("Results:", results)

if __name__ == "__main__":
    test_face_detection()
