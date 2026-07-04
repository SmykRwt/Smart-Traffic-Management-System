# Smart Traffic Management System

An AI-powered computer vision platform designed for intelligent traffic monitoring, emergency vehicle detection, and real-time traffic flow analytics. It converts generic CCTV cameras into proactive **AI Vision Agents** that understand road states, track vehicle journeys, detect stationary obstructions, and log telemetry database entries to enable smart traffic signaling.

---

## 📸 Key Features

* **Dual YOLO Inference Engine**: Employs a general YOLOv11 model for traffic analytics and a custom-trained emergency model for ambulance, firetruck, and police car detection.
* **Overlapping Duplicate Suppression**: Uses custom Intersection over Union (IoU) algorithms to eliminate duplicate bounding boxes when both models detect the same emergency vehicle.
* **Tracking ID Inheritance**: Maps tracking IDs from the general tracking model onto custom emergency detections via IoU matching, allowing emergency vehicles to be tracked seamlessly.
* **Rule & Event System**: Evaluates live telemetry data to generate structured warnings (e.g. *Heavy Traffic*, *Emergency Vehicle*, *Stopped Vehicle*) with different severity levels (`HIGH`, `MEDIUM`, `INFO`).
* **PostgreSQL Integration**: Automatically archives real-time traffic statistics and telemetry for historical analysis.
* **Premium Web Dashboard**: A dark-themed Streamlit interface featuring a live-streaming video feed, metrics grids, live vehicle distribution bar charts, and database-driven historical trend line charts.

---

## 📐 Overall Architecture

The platform processes image or video files through a sequential, modular pipeline:

```mermaid
flowchart TD
    Input[Image / Video File] --> Vision[1. Vision Engine - Dual YOLO Models]
    Vision --> Parser[2. Result Parser - Convert to Detections]
    Parser --> Duplicate[3. Duplicate Removal - IoU Suppression & ID Inheritance]
    Duplicate --> Tracking[4. Tracking - ID Persistence]
    Tracking --> Analytics[5. Analytics Engine - Telemetry Computations]
    Analytics --> Rules[6. Rule Engine - Condition Evaluation]
    Rules --> Events[7. Event Engine - Alert Generation]
    Events --> Visualization[8. Visualization - Draw Detections]
    Visualization --> HUD[9. HUD - Stats Overlay]
    HUD --> Database[10. PostgreSQL - Persistent Archival]
    HUD --> Streamlit[11. Streamlit Dashboard - UI Display]
```

---

## 📂 Project Directory Structure

```text
Smart Traffic Management System/
│
├── app/
│   ├── analytics/             # Compute metrics (FPS, congestion, density, stopped vehicles)
│   ├── core/                  # Shared configurations, BGR colors, and loggers
│   ├── database/              # SQLAlchemy database setup, models, and repositories
│   ├── detection/             # Image and video processing pipelines
│   ├── events/                # Event creation and generation engine
│   ├── models/                # Dataclasses (BoundingBox, Detection)
│   ├── rules/                 # Rules definitions and rule evaluator engine
│   ├── tracking/              # Custom ByteTrack tracking engine wrapper
│   ├── utils/                 # Visual annotations, HUD overlay, and graphics
│   └── vision/                # Vision engine and YOLO output result parsing
│
├── data/
│   └── videos/                # Sample video assets (Traffic_30sec.mp4, etc.)
│
├── models/
│   ├── yolo11n.pt             # General YOLO model weights
│   └── emergency_vehicle.pt   # Custom emergency vehicle YOLO model weights
│
├── outputs/                   # Processed video and image outputs
├── tests/                     # Unit test suite
├── main.py                    # Command-line interface entry point
├── streamlit_app.py           # Premium Streamlit web dashboard
├── requirements.txt           # Python dependencies list
└── README.md                  # Project documentation
```

---

## 🛠️ Setup & Installation

### 1. Prerequisites
* **Python 3.10+**
* **PostgreSQL** (running locally or remotely)

### 2. Configure Virtual Environment & Dependencies
Clone the repository, initialize a virtual environment, and install the required dependencies:

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Linux/macOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Database
Ensure your PostgreSQL server is running. Update the connection URL in `app/database/database.py` if necessary:
```python
DATABASE_URL = "postgresql://postgres:YOUR_PASSWORD@localhost:5432/YOUR_DB_NAME"
```

Initialize the database schema (creates the `analytics` table):
```powershell
$env:PYTHONPATH="."
python -m app.database.init_db
```

---

## 🚀 Running the Application

### 1. Web Dashboard (Streamlit)
Launch the premium, real-time live-streaming dashboard:
```powershell
streamlit run streamlit_app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser. Upload an image or video, adjust the confidence slider to refine detections, and click **Launch Vision Agent**.

### 2. Command Line Interface (CLI)
To run a batch video or image file through the terminal:
```powershell
$env:PYTHONPATH="."
python main.py
```
*Enter the file path (e.g. `data/videos/Traffic_30sec.mp4`) when prompted.*

---

## 🧪 Running Unit Tests

The project includes unit tests covering Result Parsing (inheritance checks), Stopped Vehicle detection (video clock timing), the Rule Engine, and PostgreSQL database queries.

To run the test suite:
```powershell
$env:PYTHONPATH="."
python tests/test_pipeline.py
```

---

## 💡 Core Algorithms Explained

### IoU-based Duplicate Removal & ID Inheritance
Since two YOLO models run simultaneously (General + Emergency), a single vehicle (e.g. an ambulance) is often detected twice (once as a `truck`/`car` by the general model, and once as an `ambulance` by the emergency model).
* The **Duplicate Removal** module calculates the Intersection over Union (IoU) of overlapping bounding boxes.
* If the IoU exceeds `0.50`, the general detection is discarded in favor of the emergency detection.
* Because the general model utilizes ByteTrack tracking and has a tracking ID, the emergency detection inherits this tracking ID before the general detection is deleted.

### Video-Clock Stopped Vehicle Detection
Standard algorithms detect stationary vehicles using wall-clock time (`time.time()`). This introduces false readings if inference runs faster (e.g. GPU) or slower than real-time.
* Our system tracks the current video frame index and calculates relative time: `current_time = frame_index / fps`.
* If a tracked vehicle moves less than `10 pixels` (Euclidean distance) over a duration of `6.0 seconds` (video-clock time), it is flagged as a stopped vehicle.
