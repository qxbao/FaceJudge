from flask import Flask, request, jsonify
from database import Database
from flask_cors import CORS, cross_origin
import uuid

app = Flask(__name__)
cors = CORS(app)


@app.before_request
def handle_options_preflight():
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Max-Age": "3600",
        }
        return jsonify(headers), 200


@app.route("/judge", methods=["POST"])
@cross_origin()
def judge():
    print("Received request to /judge")
    data = request.json
    if not data or "images" not in data or "age" not in data:
        print("No image or age provided in request data")
        return jsonify({"error": "No image or age provided"}), 400
    images = data["images"]
    age = data["age"]
    score = data["score"]
    print(f"Received image: {len(images)}, age: {age}, score: {score}")

    db = Database()
    profile_id, profile_folder = db.add_profile(
        age, len(images), score, str(uuid.uuid4())
    )
    db.add_profile_images(profile_id, profile_folder, images)
    db.close()
    return {"profile_id": profile_id, "profile_folder": profile_folder}


if __name__ == "__main__":
    db = Database()
    db.close()
    app.run(port=5000)
