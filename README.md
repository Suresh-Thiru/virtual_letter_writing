# virtual_letter_writing
Writing words on virtual board using openCV and identifying it using easyOCR reader

“Write It, Read It!” 🖋️🔍

Weekend Learning Project: I put open-source Python libraries together for a simple “virtual whiteboard” demo to practice computer vision and OCR, just a fun exercise.

📹 Used MediaPipe Hands + OpenCV to track my index finger and draw on a blank canvas in real time.
🔠 Integrated EasyOCR so that when I press S, the system captures the canvas and outputs the cleaned text.
✋ Added an eraser mode (five fingers up) and clear/reset on C for a smooth user experience.
🛠️ Kept it all in simple, modular Python code that’s easy to expand.

Key technical highlights:

MediaPipe for fast, accurate hand-landmark detection
OpenCV canvas blending for live “draw-over-video” visualization
EasyOCR reader with regex cleaning for reliable text extraction
Keyboard controls (S to scan, C to clear, Q to quit) for quick demo

What’s next?

This is just a fun weekend prototype, but it’s a starting point for real-world use cases like,
Hands-free cockpit input: drivers or passengers could “write” addresses or commands in mid-air (e.g., sketch a destination ZIP code), and the system would OCR and feed it into the navigation or infotainment system.
Quality inspection annotation: on the production line, inspectors could circle or mark defects in mid-air, and the OCR system would log annotations directly into the quality-control database.
Hands-free data entry on factory floors; no touchscreens needed in sterile or hazardous zones.

With some lighting robustness, performance tuning with a CNN-based handwriting model, Transformer OCR, and integration into ROS or robotic systems, this virtual whiteboard could become a nifty tool for industrial automation and beyond.


Youtube Link: https://youtu.be/aVWksC1qmEA
