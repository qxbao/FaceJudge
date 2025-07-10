from model import Model
import cv2
import face_recognition

model = Model()
image = cv2.imread('amber.jpeg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
faceloc = face_recognition.face_locations(image)
if not faceloc:
    raise ValueError("No face found in the image. Please provide an image with a face.")

face_encodings = face_recognition.face_encodings(image, faceloc)
if not face_encodings:
    raise ValueError("Could not encode the face in the image.")

face_encoding = face_encodings[0]

model.load_model('model.pkl')
print(model.predict(face_encoding, 19))