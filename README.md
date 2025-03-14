# Face-Attendance-System
A face recognition-based smart attendance system using OpenCV and Python. New users register via QR code, and their images are stored in the `known_faces` folder for automatic detection in future attendance.

## Features
- Real-time face recognition from a live CCTV feed or webcam
- QR code-based registration for new users
- Automatic attendance marking
- Web-based user registration interface
- Stores known faces for future identification

## Project Structure
```
Face_attendance_system(FAS)/
├── app.py              
├── attendance.py       
├── known_faces/       # folder of known faces 
├── attendance.csv     # attendance       
├── App.js             # react
└── Public/
    └── register.html   # Web-based registration page
```

## Installation
### Prerequisites
- Python 3.x
- OpenCV
- Face Recognition library
- Flask (for web-based registration)

### Steps
1. Clone the repository:
   ```sh
   git clone 
   cd face_attendance_system
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Run the application:
   ```sh
   python app.py
   python attendance.py
   ```
   npm start

## Usage
- Open `register.html` in a browser to register new users via QR code.
- Start the application to begin real-time face recognition.
- The system will detect faces and mark attendance automatically.

## Contributing
Feel free to submit pull requests or report issues.

## License
This project is licensed under the MIT License.

## Acknowledgments
- OpenCV for image processing
- Face Recognition library for face detection
- Flask for the web interface

