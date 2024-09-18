from flask import Flask, request, jsonify
import face_recognition
import os
import io
import base64
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dictionary to hold known face encodings and names
known_faces = []
known_names = {}

def load_known_faces():
    # Paths to the known face images and their corresponding names
    face_paths = {
        'Rajjak Ahmed': '/home/tatsuhirosatou/Desktop/1/static/person1.jpeg',
        'Debargya Dinda': '/home/tatsuhirosatou/Desktop/1/static/person2.jpeg',
        'Prakhar Kumar': '/home/tatsuhirosatou/Desktop/1/static/person3.jpeg',
        'Diganto Guha': '/home/tatsuhirosatou/Desktop/1/static/person4.jpeg',
        'Piyush Prasad': '/home/tatsuhirosatou/Desktop/1/static/person5.jpeg'
    }
    
    for name, path in face_paths.items():
        # Check if the file exists
        if not os.path.exists(path):
            print(f"File not found: {path}")
            continue
        
        # Load and encode the known face
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        
        # Check if any encodings were found
        if len(encodings) == 0:
            print(f"No face encodings found for {name}.")
            continue
        
        encoding = encodings[0]
        known_faces.append(encoding)
        known_names[encoding.tobytes()] = name

@app.route('/')
def index():
    return '''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Face Detection</title>
      </head>
      <body>
        <h1>Capture and Compare Face</h1>
        <video id="video" width="640" height="480" autoplay></video>
        <button id="capture">Capture</button>
        <canvas id="canvas" width="640" height="480"></canvas>
        <script>
          var video = document.getElementById('video');
          var canvas = document.getElementById('canvas');
          var context = canvas.getContext('2d');
          var captureButton = document.getElementById('capture');
          
          // Access the webcam
          navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
              video.srcObject = stream;
            });
          
          captureButton.addEventListener('click', function() {
            context.drawImage(video, 0, 0, 640, 480);
            var imageData = canvas.toDataURL('image/jpeg');
            fetch('/upload', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({ image: imageData }),
            })
            .then(response => response.json())
            .then(data => {
              alert('Result: ' + data.result);
            });
          });
        </script>
      </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.get_json()
    image_data = data['image']
    
    # Decode the base64 image
    image_bytes = io.BytesIO(base64.b64decode(image_data.split(',')[1]))
    image = Image.open(image_bytes)
    image = face_recognition.load_image_file(io.BytesIO(base64.b64decode(image_data.split(',')[1])))
    
    # Get face encodings
    unknown_face_encoding = face_recognition.face_encodings(image)
    
    if len(unknown_face_encoding) == 0:
        return jsonify(result='No face detected'), 400
    
    unknown_face_encoding = unknown_face_encoding[0]
    
    # Compare with known faces
    matches = face_recognition.compare_faces(known_faces, unknown_face_encoding)
    
    if True in matches:
        # Find the index of the matched face
        match_index = matches.index(True)
        # Get the name of the person
        result = list(known_names.values())[match_index]
    else:
        result = 'Face not recognized'
    
    return jsonify(result=result)

if __name__ == '__main__':
    load_known_faces()
    app.run(debug=True)
