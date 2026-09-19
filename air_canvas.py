import cv2
import numpy as np
import time
import sys
import os

# 1. Cross-platform MediaPipe Imports
try:
    import mediapipe.python.solutions.hands as mp_hands
    import mediapipe.python.solutions.drawing_utils as mp_drawing
except (ImportError, AttributeError):
    import mediapipe as mp
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

# 2. Camera Setup (DirectShow on Windows prevents instant crash)
if sys.platform.startswith("win"):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
else:
    cap = cv2.VideoCapture(0)

if not cap.isOpened():
    cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access the webcam.")
    sys.exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# 3. Canvas & Palette Configuration
canvas = None
prev_x, prev_y = 0, 0

# Colors in BGR format
COLORS = [
    (0, 0, 255),      # Neon Red
    (0, 255, 0),      # Neon Green
    (255, 255, 0),    # Cyan
    (0, 165, 255),    # Orange
    (255, 0, 255)     # Magenta
]
COLOR_NAMES = ["Red", "Green", "Cyan", "Orange", "Magenta"]
current_color_idx = 0
brush_thickness = 7
eraser_thickness = 45

# Gesture Tracking Variables
prev_wrist_x = None
swipe_cooldown = 0

# Initialize MediaPipe Hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

def count_fingers(landmarks):
    """Returns list of open states for [Index, Middle, Ring, Pinky]"""
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    fingers = []
    for tip, pip in zip(tips, pips):
        fingers.append(landmarks[tip].y < landmarks[pip].y)
    return fingers

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame. Retrying...")
        continue

    # Flip horizontally for natural mirror feel
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    if canvas is None:
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    current_color = COLORS[current_color_idx]

    # Draw Header Palette UI
    menu_h = 75
    box_w = w // len(COLORS)
    for i, col in enumerate(COLORS):
        cv2.rectangle(frame, (i * box_w, 0), ((i + 1) * box_w, menu_h), col, -1)
        # Highlight active color
        if i == current_color_idx:
            cv2.rectangle(frame, (i * box_w, 0), ((i + 1) * box_w, menu_h), (255, 255, 255), 4)
        cv2.putText(frame, COLOR_NAMES[i], (i * box_w + 30, menu_h // 2 + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        landmarks = hand_landmarks.landmark

        # Key landmark positions
        index_x, index_y = int(landmarks[8].x * w), int(landmarks[8].y * h)
        middle_x, middle_y = int(landmarks[12].x * w), int(landmarks[12].y * h)
        wrist_x = int(landmarks[0].x * w)

        fingers = count_fingers(landmarks)
        # fingers: [index, middle, ring, pinky]

        # 1. Fast Swipe Gesture (Wipe Canvas)
        if swipe_cooldown > 0:
            swipe_cooldown -= 1
        elif prev_wrist_x is not None and all(fingers):
            speed = prev_wrist_x - wrist_x
            if speed > 180:  # Fast right-to-left sweep
                canvas = np.zeros((h, w, 3), dtype=np.uint8)
                swipe_cooldown = 20
                cv2.putText(frame, "CANVAS CLEARED!", (w // 2 - 150, h // 2),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        prev_wrist_x = wrist_x

        # 2. Eraser Mode (All 4 fingers up)
        if all(fingers):
            cv2.circle(frame, (index_x, index_y), eraser_thickness // 2, (255, 255, 255), 2)
            cv2.putText(frame, "Eraser", (index_x + 15, index_y - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.circle(canvas, (index_x, index_y), eraser_thickness // 2, (0, 0, 0), -1)
            prev_x, prev_y = 0, 0

        # 3. Selection / Hover Mode (Index + Middle fingers up)
        elif fingers[0] and fingers[1] and not fingers[2] and not fingers[3]:
            prev_x, prev_y = 0, 0
            cv2.circle(frame, (index_x, index_y), 12, current_color, 2)
            cv2.circle(frame, (middle_x, middle_y), 12, current_color, 2)

            # Check menu color selection
            if index_y < menu_h:
                selected_col = index_x // box_w
                if 0 <= selected_col < len(COLORS):
                    current_color_idx = selected_col

        # 4. Drawing Mode (Only Index finger up)
        elif fingers[0] and not fingers[1] and not fingers[2] and not fingers[3]:
            cv2.circle(frame, (index_x, index_y), brush_thickness, current_color, -1)

            if index_y > menu_h:
                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = index_x, index_y

                cv2.line(canvas, (prev_x, prev_y), (index_x, index_y), current_color, brush_thickness)
                prev_x, prev_y = index_x, index_y
            else:
                prev_x, prev_y = 0, 0
        else:
            prev_x, prev_y = 0, 0

    else:
        prev_x, prev_y = 0, 0
        prev_wrist_x = None

    # Merge Canvas onto Video Stream with Glow Effect
    gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv_mask = cv2.threshold(gray_canvas, 10, 255, cv2.THRESH_BINARY_INV)
    frame_bg = cv2.bitwise_and(frame, frame, mask=inv_mask)
    output = cv2.add(frame_bg, canvas)

    cv2.imshow("Air Canvas Pro", output)

    # Key Controls
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        canvas = np.zeros((h, w, 3), dtype=np.uint8)
    elif key == ord('s'):
        filename = f"air_canvas_{int(time.time())}.png"
        cv2.imwrite(filename, canvas)
        print(f"Drawing saved as {filename}")

cap.release()
cv2.destroyAllWindows()