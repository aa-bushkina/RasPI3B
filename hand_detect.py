import threading

import cv2
import mediapipe as mp

from config import event, eventForTimer


# Запускаем в отдельном потоке по аналогии с будильником
def run_until_hand_detected(func):
    # Initializing the Model
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(static_image_mode=False, model_complexity=1, min_detection_confidence=0.75,
                          min_tracking_confidence=0.75, max_num_hands=2)

    # Start capturing video from webcam
    cap = cv2.VideoCapture(0)

    print(f"Запустили функцию, которая выключается по обнаружению руки")
    threading.Thread(target=func, daemon=True).start()

    while True:
        # Read video frame by frame
        success, img = cap.read()

        # Flip the image(frame)
        img = cv2.flip(img, 1)

        # Convert BGR image to RGB image
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process the RGB image
        results = hands.process(imgRGB)

        # If hands are present in image(frame)
        if results.multi_hand_landmarks:
            event.set()
            eventForTimer.set()
            break
        #cv2.imshow('Image', img)
        cv2.waitKey(1)
