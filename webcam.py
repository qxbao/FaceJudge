import cv2
from model import Model
import face_recognition

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0) 
model = Model()
model.load_model("model.pkl")
if not model.model:
    raise ValueError("Model not loaded. Please ensure the model is trained and saved correctly.")


if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()  
    if not ret:
        print("Error: Could not read frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) 

    cv2.imshow('Face Detection', frame)
    if len(faces) == 1:
        face_image = frame[y:y + h, x:x + w]
        face_image_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(face_image_rgb)
        
        if face_encodings:
            age = 21
            score = model.predict(face_encodings[0], age)
            print(f"Predicted score: {score}")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()