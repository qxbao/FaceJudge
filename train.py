import os
from database import Database
from model import Model
from image_processing import InputImageFolder
import numpy as np
from tqdm.auto import tqdm
import argparse

parser = argparse.ArgumentParser(description="Train the FaceJudge model")
parser.add_argument('--tune', action=argparse.BooleanOptionalAction)

tune = parser.parse_args().tune

DB_NAME = 'swipes.db'
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data') 
IMAGES_PATH = os.path.join(DATA_PATH, 'images')

training_X = []
training_Y = []
is_close = False
db = Database()

profiles = db.get_profiles()
if not profiles:
    raise ValueError("No profiles found in the database. Please add profiles before training the model.")

for profile in tqdm(profiles, desc="Processing profiles", unit="profile"):
    profile_id, age, num_images, profile_folder, score = profile
    image_folder = os.path.join(IMAGES_PATH, str(profile_folder))
    folder = InputImageFolder(image_folder)
    try:
        folder.convert_to_faces()
    except ValueError as e:
        print(f"Skipping profile ID {profile_id} due to error: {e}")
        continue
    features_mean = folder.get_features_mean()
    if features_mean is not None and np.any(features_mean):
        training_X.append([features_mean, age])
        training_Y.append(score)
    else:
        print(f"No valid features found for profile ID {profile_id} in folder {image_folder}")

model = Model()
model.set_model()
model.load_training_data([x[0] for x in training_X], [x[1] for x in training_X], training_Y)
if tune:
    model.tune_model()
model.train()
model.save_model()