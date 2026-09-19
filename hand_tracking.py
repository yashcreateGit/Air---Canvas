import cv2
import mediapipe as mp
import time

print("1. Loading MediaPipe...")
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

print("2. Opening Camera...")
cap = cv2.VideoCapture(0)
time.sleep(2) # Give macOS camera extra time to warm up

if not cap.isOpened():
    print("ERROR: Camera failed to open. Check macOS permissions.")
    exit()

print("3. Camera running! Look for the new window. Press 'q' to quit.")
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Warning: Camera returned an empty frame, waiting...")
        cv2.waitKey(100)
        continue

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Air Canvas", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("4. Script closed cleanly.")
