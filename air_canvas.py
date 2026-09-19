import cv2
import mediapipe as mp
import numpy as np
import time
import math
import os

# Setup MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
time.sleep(1)

canvas = None
prev_pts = [(0, 0), (0, 0)]
prev_palm_x = [0, 0]

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
paint_color = colors[0]
last_save_time = 0
take_snapshot = False

def get_distance(lm1, lm2):
    return math.hypot(lm1.x - lm2.x, lm1.y - lm2.y)

while cap.isOpened():
    success, frame = cap.read()
    if not success: continue
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    take_snapshot = False
    
    if canvas is None: canvas = np.zeros_like(frame)

    # UI: Buttons and Colors
    cv2.rectangle(frame, (40, 10), (200, 90), (122, 122, 122), cv2.FILLED)
    cv2.putText(frame, "CLEAR", (70, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    
    cv2.rectangle(frame, (220, 10), (380, 90), (100, 150, 100), cv2.FILLED)
    cv2.putText(frame, "SAVE", (260, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    cv2.rectangle(frame, (420, 10), (570, 90), colors[0], cv2.FILLED)
    cv2.rectangle(frame, (590, 10), (740, 90), colors[1], cv2.FILLED)
    cv2.rectangle(frame, (760, 10), (910, 90), colors[2], cv2.FILLED)
    cv2.rectangle(frame, (930, 10), (1080, 90), colors[3], cv2.FILLED)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    current_mode = "HOVER"

    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            if i >= 2: break
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            lm = hand_landmarks.landmark
            
            fingers = []
            for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
                fingers.append(1 if get_distance(lm[tip], lm[0]) > get_distance(lm[pip], lm[0]) else 0)

            ix, iy = int(lm[8].x * w), int(lm[8].y * h)
            px, py = int(lm[9].x * w), int(lm[9].y * h)
            
            # 1. DRAW / CLICK MODE
            if fingers == [1, 0, 0, 0]:
                current_mode = "DRAWING / CLICKING"
                cv2.circle(frame, (ix, iy), 10, paint_color, cv2.FILLED)
                
                if iy <= 100: 
                    prev_pts[i] = (0, 0)
                    if 40 <= ix <= 200: canvas = np.zeros_like(frame)
                    elif 220 <= ix <= 380:
                        if time.time() - last_save_time > 2:
                            take_snapshot = True # Trigger save at the end of the frame
                    elif 420 <= ix <= 570: paint_color = colors[0]
                    elif 590 <= ix <= 740: paint_color = colors[1]
                    elif 760 <= ix <= 910: paint_color = colors[2]
                    elif 930 <= ix <= 1080: paint_color = colors[3]
                else: 
                    if prev_pts[i] == (0, 0): prev_pts[i] = (ix, iy)
                    cv2.line(canvas, prev_pts[i], (ix, iy), paint_color, 8)
                    prev_pts[i] = (ix, iy)

            # 2. ERASE / SWIPE MODE
            elif fingers == [1, 1, 1, 1]:
                current_mode = "ERASING / SWIPE"
                cv2.circle(frame, (px, py), 60, (255, 255, 255), 2)
                cv2.circle(canvas, (px, py), 60, (0, 0, 0), cv2.FILLED)
                prev_pts[i] = (0, 0)
                
                if prev_palm_x[i] != 0 and prev_palm_x[i] - px > 150:
                    canvas = np.zeros_like(frame)
                prev_palm_x[i] = px
            else:
                prev_pts[i] = (0, 0)
                prev_palm_x[i] = 0
    else:
        prev_pts = [(0, 0), (0, 0)]
        prev_palm_x = [0, 0]
        current_mode = "NO HAND DETECTED"

    # Apply NEON GLOW EFFECT
    # Blur the canvas and add it back to itself to create a glowing halo
    glow = cv2.GaussianBlur(canvas, (27, 27), 0)
    glowing_canvas = cv2.addWeighted(canvas, 1.0, glow, 1.0, 0)

    # Merge the glowing canvas onto the camera feed
    merged = cv2.add(frame, glowing_canvas)

    # Handle Saving the FULL Merged Image to the Desktop
    if take_snapshot:
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        filename = os.path.join(desktop_path, f"AirCanvas_{int(time.time())}.png")
        cv2.imwrite(filename, merged)
        print(f"SUCCESS: Image saved directly to your Desktop -> {filename}")
        last_save_time = time.time()

    if time.time() - last_save_time < 2:
        cv2.putText(merged, "SAVED TO DESKTOP!", (400, 360), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 255, 0), 3)

    cv2.putText(merged, f"MODE: {current_mode}", (30, 680), cv2.FONT_HERSHEY_SIMPLEX, 1, paint_color, 3)

    cv2.imshow("Air Canvas Pro", merged)

    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
