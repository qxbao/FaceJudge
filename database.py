import os
import sqlite3
import uuid
import base64

DB_NAME = 'swipes.db'
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data') 
IMAGES_PATH = os.path.join(DATA_PATH, 'images')

class Database:
    def __init__(self) -> None:
        self.db_path = os.path.join(DATA_PATH, DB_NAME)
        self.conn = sqlite3.connect(self.db_path)
        self.__init_db()
        
    def get_profiles(self) -> list[any]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM profiles')
        return cursor.fetchall()
    
    def add_profile(self, age, num_images, score, profile_folder=uuid.uuid4()) -> tuple[int, str]:
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO profiles (age, num_images, profile_folder, score)
            VALUES (?, ?, ?, ?)
        ''', (age, num_images, str(profile_folder), score))
        self.conn.commit()
        os.makedirs(os.path.join(IMAGES_PATH, str(profile_folder)), exist_ok=True)
        profile_id = cursor.lastrowid
        return (profile_id, str(profile_folder))

    def add_profile_images(self, profile_id, profile_folder, images) -> None:
        cursor = self.conn.cursor()
        image_path = os.path.join(IMAGES_PATH, str(profile_folder))
        os.makedirs(image_path, exist_ok=True)
        for order, image in enumerate(images):
            cursor.execute('''
                INSERT INTO profile_images (profile_id, image_order)
                VALUES (?, ?)
            ''', (profile_id, order))
            if "data:image" in image:
                image = image.split(",")[1]
            decoded_image_data = base64.b64decode(image)
            image_file_path = os.path.join(image_path, f'{order}.jpg')
            with open(image_file_path, 'wb') as f:
                f.write(decoded_image_data)
                f.close()
        self.conn.commit()
        
    def close(self) -> None:
        if self.conn:
            self.conn.close()

    @staticmethod
    def __init_db() -> None:
        os.makedirs(IMAGES_PATH, exist_ok=True)
        open(os.path.join(DATA_PATH, DB_NAME), 'a').close()
        
        conn = sqlite3.connect(os.path.join(DATA_PATH, DB_NAME))
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                age INTEGER NOT NULL,
                num_images INTEGER NOT NULL,
                profile_folder TEXT NOT NULL,
                score REAL NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profile_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL,
                image_order INTEGER NOT NULL,
                FOREIGN KEY (profile_id) REFERENCES profiles(id)
            )
        ''')
        conn.commit()
