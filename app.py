from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Create known_faces directory if not exists
KNOWN_FACES_DIR = "known_faces"
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    photo = request.files.get("photo")

    if not name or not photo:
        return jsonify({"error": "⚠ Please enter a name and upload a photo!"}), 400

    # Save the image as name.jpg
    photo_path = os.path.join(KNOWN_FACES_DIR, f"{name}.jpg")
    photo.save(photo_path)

    return jsonify({"message": f"✅ {name} registered successfully!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)