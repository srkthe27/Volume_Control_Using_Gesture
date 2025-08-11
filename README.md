# ✋ Hand Tracking + Volume Control

A Python project that uses **MediaPipe** hand tracking and **OpenCV** to control system volume with hand gestures.

Includes two main scripts:

- **`hand_tracking_module.py`** — Reusable hand‑tracking module with a demo runner.
- **`volume_control.py`** — Uses the hand‑tracking module to control Windows system volume (via `pycaw`).

> **Note:** `volume_control.py` works only on **Windows** because it uses Windows Core Audio APIs via `pycaw`.  
> `hand_tracking_module.py` works cross‑platform.

---

## 📥 1. Clone the repository
```bash
git clone https://github.com/srkthe27/Volume_Control_Using_Gesture.git
cd Volume_Control_Using_Gesture
```

---

## 🛠 2. Create & activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (cmd):**
```cmd
python -m venv .venv
.\.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 📦 3. Install dependencies
With your virtual environment active:
```bash
pip install -r requirements.txt
```

If you do not have a `requirements.txt`, create it with:
```
mediapipe
opencv-python
numpy
pycaw
comtypes
```
Then:
```bash
pip install -r requirements.txt
```

---

## 📂 Project Files

### `hand_tracking_module.py`
- Contains the `HandDetector` class.
- Key methods:
  - `findHands(frame, draw=True)` → Processes a frame and optionally draws hand landmarks.
  - `find_position(frame, hand_no=0, draw=True)` → Returns a list of landmark coordinates.
- Includes a `main()` function to test hand detection via webcam.

### `volume_control.py`
- Imports `HandDetector` from `hand_tracking_module.py`.
- Detects thumb tip (landmark **id 4**) and index tip (**id 8**).
- Measures the distance between them and maps it to system volume.
- Displays an on-screen volume bar and percentage.

⚠ **Important:** The file must be named **exactly**:
```
hand_tracking_module.py
```
If not, rename it or update this line in `volume_control.py` accordingly:
```python
import hand_tracking_module as htm
```

---

## ▶ How to Run

### **Test hand tracking** (cross-platform)
```bash
python hand_tracking_module.py
```
- Opens a webcam window with hand landmarks drawn.
- Press **`d`** to exit.

### **Run volume control** (Windows only)
```bash
python volume_control.py
```
- Use the distance between thumb and index finger to control system volume.
- Press **`d`** to exit.

---

## 🔧 Troubleshooting

- **`ModuleNotFoundError: No module named 'hand_tracking_module'`**  
  Make sure the file is in the same folder and correctly named.

- **Black screen / webcam not detected**  
  Adjust the camera index:
  ```python
  cap = cv.VideoCapture(0)  # Try using 1, 2, etc.
  ```

- **Mediapipe installation issues**  
  Update `pip`:
  ```bash
  python -m pip install --upgrade pip
  ```

- **`pycaw` fails on Linux/macOS**  
  Use Windows or replace with platform-specific audio control APIs.

---

## ⚡ Quick Start Commands
```bash
git clone https://github.com/srkthe27/Volume_Control_Using_Gesture.git
cd Volume_Control_Using_Gesture
python -m venv .venv
.\.venv\Scripts\activate   # (Windows)
pip install -r requirements.txt
python hand_tracking_module.py
python volume_control.py   # (Windows only)
```

---

## 📜 License
This project is licensed under the **MIT License**. Feel free to customize or update as needed.
