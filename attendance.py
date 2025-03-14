import cv2
import face_recognition
import numpy as np
import qrcode
from pyzbar import pyzbar
import os
import csv
from datetime import datetime

KNOWN_FACES_DIR = "known_faces"  # Add known_face folder
ATTENDANCE_LOG = "attendance.csv" # Add CSV 
TOLERANCE = 0.5 # Lower values mean stricter matching

def resize(img, size):
    width = int(img.shape[1] * size)
    height = int(img.shape[0] * size)
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

def find_encoding(images):
    encodings = []
    for img in images:
        img = resize(img, 0.50)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        if encode:
            encodings.append(encode[0])
        else:
            print("⚠ Warning: No face detected in one of the images.")
    return encodings

def load_known_faces():
    known_faces = []
    known_names = []
    if not os.path.exists(KNOWN_FACES_DIR):
        os.makedirs(KNOWN_FACES_DIR)
    
    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.endswith((".jpg", ".png")):
            image = cv2.imread(os.path.join(KNOWN_FACES_DIR, filename))
            if image is not None:
                known_faces.append(image)
                known_names.append(os.path.splitext(filename)[0])
            else:
                print(f"⚠ Warning: Unable to load {filename}")
    
    return find_encoding(known_faces), known_names

def is_attendance_marked(name):
    today = datetime.now().strftime("%Y-%m-%d")
    if os.path.exists(ATTENDANCE_LOG):
        with open(ATTENDANCE_LOG, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == name and row[1].startswith(today):
                    return True
    return False

def mark_attendance(name):
    if not is_attendance_marked(name):
        with open(ATTENDANCE_LOG, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        print(f"✅ Attendance marked for {name}.")
    else:
        print(f"⚠ {name} has already been marked present today.")

def scan_qr_code(frame):
    decoded_objects = pyzbar.decode(frame)
    for obj in decoded_objects:
        return obj.data.decode("utf-8")
    return None

def check_for_new_faces():
    global known_face_encodings, known_face_names
    current_files = {os.path.splitext(f)[0] for f in os.listdir(KNOWN_FACES_DIR) if f.endswith((".jpg", ".png"))}
    
    if set(known_face_names) != current_files:
        print("🔄 New face detected! Updating encodings...")
        known_face_encodings, known_face_names = load_known_faces()

# Load known faces
known_face_encodings, known_face_names = load_known_faces()
video_capture = cv2.VideoCapture(0)

# Generate QR code
registration_url = "http://localhost:3001/register.html"
qr = qrcode.make(registration_url)
qr.save("registration_qr.png")
qr_img = cv2.imread("registration_qr.png")
qr_img = resize(qr_img, 0.3)

while True:
    check_for_new_faces()  # 🔄 Check for new images in the folder
    
    ret, frame = video_capture.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_h, frame_w, _ = frame.shape
    
    # Header for the system (Centered)
    cv2.putText(frame, "Face Attendance System", (frame_w // 3, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
    
    # QR Code UI section with styling
    qr_x_offset = frame_w - qr_img.shape[1] - 40
    qr_y_offset = frame_h // 4
    
    overlay = frame.copy()
    cv2.rectangle(overlay, (qr_x_offset - 20, qr_y_offset - 40), (qr_x_offset + qr_img.shape[1] + 20, qr_y_offset + qr_img.shape[0] + 20), (50, 50, 200), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    
    frame[qr_y_offset:qr_y_offset + qr_img.shape[0], qr_x_offset:qr_x_offset + qr_img.shape[1]] = qr_img
    cv2.putText(frame, " Scan Me to Register", (qr_x_offset - 20, qr_y_offset - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(distances) if len(distances) > 0 else -1
        
        if best_match_index != -1 and distances[best_match_index] < TOLERANCE:
            name = known_face_names[best_match_index]
            mark_attendance(name)
        else:
            name = "Unknown"

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    cv2.imshow("Face Attendance System", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()