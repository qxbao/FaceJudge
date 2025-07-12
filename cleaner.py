import cv2
import os
from database import Database
import face_recognition
from tqdm import tqdm

dirs = os.listdir(os.path.join(os.path.dirname(__file__), 'data', 'images'))
path = os.path.join(os.path.dirname(__file__), 'data', 'images')

def clean_empty_images():
    db = Database()
    for dir in tqdm(dirs, desc="Cleaning empty images", unit="dir"):
        dir_path = os.path.join(path, dir)
        for file in os.listdir(dir_path):
            if file.endswith('.jpg'):
                file_path = os.path.join(dir_path, file)
                image = cv2.imread(file_path)
                if image is None or not image.flatten().any():
                    os.remove(file_path)
                    conn = db.conn
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM profile_images WHERE image_order = ? AND profile_id = ?', (file.split('.')[0], dir))
                    conn.commit()      
    db.close()

def clean_noface_images():
    db = Database()
    for dir in tqdm(dirs, desc="Cleaning images with no faces", unit="dir"):
        dir_path = os.path.join(path, dir)
        for file in os.listdir(dir_path):
            if file.endswith('.jpg'):
                file_path = os.path.join(dir_path, file)
                image = cv2.imread(file_path)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                if image is None:
                    continue
                face_locations = face_recognition.face_locations(image)
                if len(face_locations) == 0:
                    os.remove(file_path)
                    conn = db.conn
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM profile_images WHERE image_order = ? AND profile_id = ?', (file.split('.')[0], dir))
                    conn.commit()
    db.close()

def clean_empty_directories():
    for dir in dirs:
        dir_path = os.path.join(path, dir)
        if not os.listdir(dir_path):
            print(f"Removing empty directory: {dir_path}")
            os.rmdir(dir_path)

def sync_database():
    dirs = os.listdir(os.path.join(os.path.dirname(__file__), 'data', 'images'))
    db = Database()
    conn = db.conn
    cursor = conn.cursor()
    db_dir = cursor.execute('SELECT profile_folder FROM profiles').fetchall()
    
    for dir in db_dir:
        if dir[0] not in dirs:
            print(f"Removing profile folder: {dir[0]}")
            cursor.execute('DELETE FROM profiles WHERE profile_folder = ?', (dir[0],))
            conn.commit()
            dir_path = os.path.join(path, dir[0])
            if os.path.exists(dir_path):
                os.rmdir(dir_path)
    for dir in dirs:
        if dir not in [dir[0] for dir in db_dir]:
            num_images = len(os.listdir(os.path.join(path, dir)))
            print("LOST PROFILE FOLDER: ", dir)
            score = input("Enter score for lost profile folder: ")
            age = input("Enter age for lost profile folder: ")
            db.add_profile(age, num_images, score, dir)
            for image in os.listdir(os.path.join(path, dir)):
                if image.endswith('.jpg'):
                    cursor.execute('INSERT INTO profile_images (profile_id, image_order) VALUES (?, ?)', (dir, image.split('.')[0]))
    db.close()

if __name__ == "__main__":
    clean_empty_images()
    print("Empty images cleaned up.")
    clean_noface_images()
    print("Images with no faces cleaned up.")
    clean_empty_directories()
    print("Empty directories cleaned up.")
    sync_database()
    print("Database synchronized with image directories.")