import cv2

# Initialize webcam (0 is the built-in FaceTime camera)
cap = cv2.VideoCapture(0)

# Set resolution width and height
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("Starting camera... Press 'q' on your keyboard inside the window to exit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip the frame horizontally so it acts like a mirror
    frame = cv2.flip(frame, 1)

    # Display the live feed in a window
    cv2.imshow("Air Canvas - Camera Test", frame)

    # Exit when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close open windows
cap.release()
cv2.destroyAllWindows()
