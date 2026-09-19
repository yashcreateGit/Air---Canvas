import cv2
import mediapipe as mp
import time

print("1. Testing MediaPipe init...")
hands = mp.solutions.hands.Hands(max_num_hands=2)
print("   MediaPipe initialized.")

print("2. Testing camera indices...")
for idx in [0, 1]:
    cap = cv2.VideoCapture(idx)
    time.sleep(0.5)
    opened = cap.isOpened()
    ret, frame = cap.read() if opened else (False, None)
    print(f"   Index {idx} -> isOpened: {opened}, read(): {ret}")
    cap.release()
