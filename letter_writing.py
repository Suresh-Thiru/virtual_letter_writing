import cv2
import numpy as np
import mediapipe as mp
import easyocr
import re

hands_detector = mp.solutions.hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7)

text_reader = easyocr.Reader(['en'])

canvas = np.ones((480, 640, 3), dtype=np.uint8) * 255

prev_point = None

recognized_text = ""

def count_fingers(hand_landmarks, hand_label):
    fingers_up = 0
    tip_ids = [8, 12, 16, 20]

    if hand_label == "Right":
        if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
            fingers_up += 1
    else:
        if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x:
            fingers_up += 1

    for tip in tip_ids:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers_up += 1

    return fingers_up


def get_text_from_canvas(image):

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = text_reader.readtext(rgb_image)
    text = " ".join([res[1] for res in result])
    return text

def clean_and_format_text(text):
    text = text.upper()
    filtered_text = re.sub(r'[^A-Z ]', '', text)
    return filtered_text

camera = cv2.VideoCapture(0)

print("Camera is ready")

while camera.isOpened():
    ret, frame = camera.read()

    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands_detector.process(rgb_frame)


    if results.multi_hand_landmarks:
        for hand_landmarks, hand_info in zip(results.multi_hand_landmarks, results.multi_handedness):
            hand_label = hand_info.classification[0].label

            fingers_up = count_fingers(hand_landmarks, hand_label)

            x_pos = int(hand_landmarks.landmark[8].x * frame_width)
            y_pos = int(hand_landmarks.landmark[8].y * frame_height)

            cv2.circle(frame, (x_pos, y_pos), 8, (0, 255, 0), -1)

            if fingers_up == 5:

                cv2.circle(canvas, (x_pos, y_pos), 20, (255, 255, 255), -1)
                cv2.putText(frame, "Eraser Mode", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                prev_point = None

            elif fingers_up == 1:
                if prev_point is None:
                    prev_point = (x_pos, y_pos)
                else:
                    cv2.line(canvas, prev_point, (x_pos, y_pos), (0, 0, 0), 4)
                    prev_point = (x_pos, y_pos)
            else:
                prev_point = None
    else:
        prev_point = None

    blended_frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)


    if recognized_text:
        cv2.rectangle(blended_frame, (250, 10), (620, 70), (0, 0, 0), -1)
        cv2.putText(blended_frame, "Text:" + recognized_text, (270, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


    cv2.imshow("Virtual Drawing Board", blended_frame)


    key = cv2.waitKey(1) & 0xFF


    if key == ord('q'):

        break
    elif key == ord('s'):

        print("Recognizing text...")
        text = get_text_from_canvas(canvas)

        recognized_text = clean_and_format_text(text)
        print(f"Recognized Text: {recognized_text}")
    elif key == ord('c'):

        canvas[:] = 255
        recognized_text = ""

camera.release()
cv2.destroyAllWindows()
