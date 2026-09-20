# Air Canvas Pro 🎨✨

An interactive, touchless digital canvas built with Python. Air Canvas Pro uses computer vision to track hand landmarks in real-time, allowing users to draw, change colors, and erase entirely through hand gestures—no mouse, keyboard, or drawing tablet required.

### 🚀 Features
* **Real-Time Hand Tracking:** Utilizes Google MediaPipe for high-speed, rotation-invariant hand landmark detection.
* **Gestural UI:** Switch between drawing, menu selection, and erasing purely based on finger positioning and palm velocity.
* **Interactive Color Palette:** Hover over virtual buttons on the camera feed to change brush colors or clear the screen.
* **Save Functionality:** Instantly export your digital artwork as a `.png` file.
* **Neon Glow Engine:** Applies an algorithmic Gaussian blur over the digital ink canvas to create a vibrant neon aesthetic.
* **Cross-Platform:** Available as a zero-installation live web app or a high-performance local desktop application.

### 🛠 Tech Stack
* **Languages:** Python 3, JavaScript, HTML/CSS
* **OpenCV (cv2):** Image processing, frame manipulation, and UI rendering.
* **MediaPipe:** Spatial mapping and hand-tracking machine learning pipeline.
* **NumPy:** High-performance matrix calculations for the drawing canvas logic.

---

## 🚀 Getting Started: 2 Ways to Use

### Method 1: Instant Web Access (No Installation Required)
You can try the project directly inside any modern browser (Chrome, Edge, Safari, Brave) using your device's GPU.

1. **Open the Live Application:** 👉 [Launch Air Canvas Pro Web](https://yashcreateGit.github.io/Air---Canvas/)
2. **Grant Camera Permissions:** When prompted by your browser, click **Allow** to enable webcam access.
3. **Start Drawing:** Position your hand inside the camera frame to control the virtual canvas.

### Method 2: Run Locally (Desktop Version)
To download the source code and run the standalone Python application on Windows or macOS, follow these steps in your Terminal or Command Prompt:

1. Clone the repository:
   git clone https://github.com/yashcreateGit/Air---Canvas.git

2. Navigate into the folder:
   cd Air---Canvas

3. Install the dependencies:
   pip install -r requirements.txt

4. Run the application:
   python air_canvas.py

---

## ✋ Hand Gestures & Controls

| Gesture | Action | Description |
| :--- | :--- | :--- |
| **☝️ Index Finger Up** | **Draw / Select** | Draws ink on the canvas. If hovering over the top menu, it selects a UI button or color. |
| **✌️ Index + Middle Up** | **Hover Mode** | Moves the pointer without drawing. Use this to safely navigate between colors. |
| **🖐️ 4 Fingers Up (Open Palm)** | **Eraser Tool** | Turns your hand into a precision eraser to wipe specific strokes. |
| **👋 Open Palm + Fast Swipe** | **Clear Canvas** | Rapidly sweep your hand right-to-left to instantly wipe the entire board. |

## ⌨️ Keyboard Shortcuts (Local Desktop Version)
- **`q`** — Quit and safely close the camera window.
- **`c`** — Clear the entire canvas.
- **`s`** — Save a high-resolution screenshot (`.png`) of your artwork directly to your project folder.

---

## ❓ Troubleshooting

- **Webcam light doesn't turn on (Desktop):** Ensure Windows/macOS Camera Privacy settings permit desktop applications to access the camera.
- **Web version shows a black screen:** Click the padlock icon in your browser's address bar, make sure camera permissions are set to **Allow**, and refresh the page.
