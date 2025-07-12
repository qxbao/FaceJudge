import argparse
from model import Model
import cv2
import face_recognition

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default="model.pkl", help='Path to the trained model file')
parser.add_argument('--image', type=str, default="input.jpg", help='Path to the image file')
parser.add_argument('--age', type=int, required=True, help='Age of the person in the image')

args = parser.parse_args()
image, age , model_path = args.image, args.age, args.model

model = Model()
image = cv2.imread(image)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
faceloc = face_recognition.face_locations(image)
if len(faceloc) != 1:
    raise ValueError("No face or too many faces found in the image. Please provide an image with a face.")

face_encodings = face_recognition.face_encodings(image, faceloc)
if not face_encodings:
    raise ValueError("Could not encode the face in the image.")

face_encoding = face_encodings[0]

model.load_model(model_path)
print(f"This face's point: {model.predict(face_encoding, int(age))}")