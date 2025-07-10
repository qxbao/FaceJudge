from flask import Flask, render_template, request, jsonify, redirect
import os
from database import Database
import base64

app = Flask(__name__)
imgDir = os.path.join(os.path.dirname(__file__), 'static', 'img')
imgs = os.listdir(imgDir)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE',])
def index():
    age = imgs[0].split('_')[0]
    return render_template('index.html', img=imgs[0], age=age)

@app.route('/judge', methods=['POST'])
def judge():
    import uuid
    data = request.get_json(force=True)
    print("Received data:", data)
    if not data or 'image' not in data or 'age' not in data:
        print("No image or age provided in request data")
        return jsonify({'error': 'No image or age provided'}), 400    
    image_name = data['image']
    age = data['age']
    score = data['score']
    print(f"Received image: {image_name}, age: {age}, score: {score}")
    if image_name not in imgs:
        return jsonify({'error': 'Image not found'}), 401

    db = Database()
    profile_id, profile_folder = db.add_profile(age, 1, score, str(uuid.uuid4()))
    with open(os.path.join(os.path.dirname(__file__), 'static', 'img', image_name), 'rb') as f:
        image = f.read()
        img = base64.b64encode(image).decode('utf-8')
        data_uri = f"data:image/jpg;base64,{img}"
        db.add_profile_images(profile_id, profile_folder, [data_uri])
        db.close()
        imgs.pop(0)
        f.close()
        return {
            'profile_id': profile_id,
            'profile_folder': profile_folder
        }

if __name__ == "__main__":
    app.run(debug=True, port=5000)