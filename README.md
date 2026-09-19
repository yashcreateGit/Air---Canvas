# Air Canvas Pro 🎨✨

An interactive, touchless digital canvas built with Python. Air Canvas Pro uses computer vision to track hand landmarks in real-time, allowing users to draw, change colors, and erase entirely through hand gestures—no mouse or keyboard required.

### 🚀 Features
* **Real-Time Hand Tracking:** Utilizes Google MediaPipe for high-speed, rotation-invariant hand landmark detection.
* **Gestural UI:** Switch between drawing, menu selection, and erasing purely based on finger positioning and palm velocity.
* **Interactive Color Palette:** Hover over virtual buttons on the camera feed to change brush colors or clear the screen.
* **Save Functionality:** Hover over the virtual save button to instantly export your artwork to your Desktop as a `.png`.
* **Neon Glow Engine:** Applies an algorithmic Gaussian blur over the digital ink canvas to create a vibrant neon aesthetic.

### 🛠 Tech Stack
* **Python 3**
* **OpenCV (cv2):** Image processing, frame manipulation, and UI rendering.
* **MediaPipe:** Spatial mapping and hand-tracking machine learning pipeline.
* **NumPy:** High-performance matrix calculations for the drawing canvas logic.

### 🖐 Controls & Gestures
| Gesture | Action |
| :--- | :--- |
| **Index Finger Up** | Draw ink on the canvas or select a UI button. |
| **Hover Top Menu** | Change colors, Clear Canvas, or Save to Desktop. |
| **Open Palm (4 Fingers Up)** | Activates the Eraser tool. |
| **Open Palm + Fast Swipe** | Rapidly swipe right-to-left to instantly wipe the canvas. |

### 💻 How to Run Locally

1. **Clone the repository**
2. **Install dependencies**
cat << 'EOF' > README.md
# Air Canvas Pro 🎨✨

An interactive, touchless digital canvas built with Python. Air Canvas Pro uses computer vision to track hand landmarks in real-time, allowing users to draw, change colors, and erase entirely through hand gestures—no mouse or keyboard required.

### 🚀 Features
* **Real-Time Hand Tracking:** Utilizes Google MediaPipe for high-speed, rotation-invariant hand landmark detection.
* **Gestural UI:** Switch between drawing, menu selection, and erasing purely based on finger positioning and palm velocity.
* **Interactive Color Palette:** Hover over virtual buttons on the camera feed to change brush colors or clear the screen.
* **Save Functionality:** Hover over the virtual save button to instantly export your artwork to your Desktop as a `.png`.
* **Neon Glow Engine:** Applies an algorithmic Gaussian blur over the digital ink canvas to create a vibrant neon aesthetic.

### 🛠 Tech Stack
* **Python 3**
* **OpenCV (cv2):** Image processing, frame manipulation, and UI rendering.
* **MediaPipe:** Spatial mapping and hand-tracking machine learning pipeline.
* **NumPy:** High-performance matrix calculations for the drawing canvas logic.

### 🖐 Controls & Gestures
| Gesture | Action |
| :--- | :--- |
| **Index Finger Up** | Draw ink on the canvas or select a UI button. |
| **Hover Top Menu** | Change colors, Clear Canvas, or Save to Desktop. |
| **Open Palm (4 Fingers Up)** | Activates the Eraser tool. |
| **Open Palm + Fast Swipe** | Rapidly swipe right-to-left to instantly wipe the canvas. |

### 💻 How to Run Locally

1. Clone the repository:
    git clone https://github.com/YOUR_USERNAME/air-canvas.git
    cd air-canvas

2. Install dependencies:
    pip install opencv-python mediapipe numpy

3. Run the application:
    python air_canvas.py
