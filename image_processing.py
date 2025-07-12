import os
import cv2
import face_recognition
import numpy as np

class InputImageFolder:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.images = []
        self.features = []
        self.__load_images()

    def __load_images(self):
        """Load images from the folder"""
        for filename in os.listdir(self.folder_path):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(self.folder_path, filename)
                image = cv2.imread(image_path)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                if image is not None:
                    self.images.append(image)

    def convert_to_faces(self, t=0):
        """Preprocess images for face recognition. DO NOT specify 't' parameter."""
        if t > len(self.images):
            raise ValueError("No single-face image found after attempts.")
        known_faces = []
        face_models = []
        for index, image in enumerate(self.images):
            face_locations = face_recognition.face_locations(image)
            if len(face_locations) == 0:
                continue
            elif len(face_locations) > 1:
                if index == 0:
                    self.images.append(image)
                    self.images = self.images[:index] + self.images[index + 1:]
                    return self.convert_to_faces(t+1)
                else:
                    for index, face_location in enumerate(face_locations):
                        face = face_recognition.face_encodings(
                            image, [face_location])[0]
                        comparison = face_recognition.compare_faces(
                            face_models, face)
                        if True in comparison:
                            face_models.append(face)
                            top, right, bottom, left = face_location
                            known_faces.append(image[top:bottom, left:right])
                            break
            else:
                top, right, bottom, left = face_locations[0]
                face = face_recognition.face_encodings(
                    image, [face_locations[0]])[0]
                face_models.append(face)
                known_faces.append(image[top:bottom, left:right])
        self.features = face_models
        self.images = known_faces

    def export_output(self):
        """Export the processed images to the /output folder"""
        os.makedirs(self.folder_path + '/output', exist_ok=True)
        for i, image in enumerate(self.images):
            output_path = os.path.join(
                self.folder_path, 'output', f'image_{i}.jpg')
            cv2.imwrite(output_path, image)

    def get_features_mean(self):
        """Export the features of the processed images"""
        return np.mean(self.features, axis=0) if self.features else np.zeros(128)