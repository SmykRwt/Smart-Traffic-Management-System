# 🚦 AI Smart Traffic Management System

An intelligent, computer-vision powered platform for real-time traffic monitoring, congestion assessment, emergency vehicle prioritization, and database logging. 

---

## 🎬 Project Showcase

See the AI Traffic Agent in action, tracking vehicles, detecting stopped obstructions, and alerting the control center.


![Traffic Detection Output](data/Output/Screenshot%202026-07-04%20185917.png)

<br><br><br><br>

### 📸 Live Detection Frame
![Traffic Detection Output](data/Output/result.jpg)

---

## 🚀 Key Features

* **Dual YOLO Vision Engine**: Runs a general model for standard traffic tracking alongside a specialized emergency model.
* **Emergency Vehicle Classification**: Customized model trained to identify and prioritize **3 emergency vehicle classes**:
  * **Ambulance**
  * **Fire Truck**
  * **Police Car**
* **Duplicate Suppression & ID Inheritance**: Resolves overlap conflicts using custom IoU matching. Emergency vehicles inherit tracking IDs from the general engine, ensuring smooth telemetry tracing.
* **Video-Clock Time Sync**: Stopped-vehicle timers use video frame rates instead of system wall clocks, maintaining accuracy regardless of processing speeds.
* **Real-time Event Rules Engine**: Automatically triggers warnings (`HIGH`, `MEDIUM`, `INFO`) based on congestion, stationary vehicles, or emergency dispatch events.
* **PostgreSQL Integration**: Logs traffic stats and telemetry indicators periodically for historical trend forecasting.
* **Premium Dark Dashboard**: Built with Streamlit, containing live streams, interactive controls, live distribution metrics, and trend charts.

---

## 📐 Pipeline Architecture

The processing pipeline is modular and sequential:

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

## 📂 Codebase Layout

```text
Smart Traffic Management System/
│
├── app/
│   ├── analytics/             # Compute metrics (FPS, congestion, density, stopped vehicles)
│   ├── core/                  # Configurations, custom logger, colors
│   ├── database/              # DB repository, SQLAlchemy connections, schemas
│   ├── detection/             # Pipeline processors for files and frames
│   ├── events/                # Alert generation engine
│   ├── models/                # Dataclasses (Detection, BoundingBox)
│   ├── rules/                 # Rules definitions and evaluation engine
│   ├── tracking/              # ByteTrack engine integration
│   ├── utils/                 # Visual annotation utilities (bounding boxes, HUD overlays)
│   └── vision/                # YOLO integrations, parser, and duplicate suppression
│
├── data/
│   └── videos/                # Sample video assets (Traffic_30sec.mp4, Traffic_2min.mp4)
│
├── models/
│   ├── yolo11n.pt             # General YOLO model weights
│   └── emergency_vehicle.pt   # Custom emergency vehicle YOLO model weights
│
├── tests/                     # Pipeline unit tests
├── main.py                    # CLI app launcher
├── streamlit_app.py           # Web Dashboard app launcher
├── requirements.txt           # Python dependencies list
└── README.md                  # System documentation
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites
* **Python 3.10+**
* **PostgreSQL** Database running locally/remotely.

### 2. Configure Virtual Environment & Dependencies
```powershell
# Create & Activate Virtual Environment
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows (PowerShell)
source .venv/bin/activate     # macOS/Linux

# Install all requirements
pip install -r requirements.txt
```

### 3. Setup PostgreSQL Database
Ensure your PostgreSQL instance is running. Create a database named `ai_vision`. 

The configuration URL in [app/database/database.py](file:///c:/Users/rawat/Desktop/My%20Projects/Smart%20Traffic%20Management%20System/app/database/database.py) defaults to:
```python
DATABASE_URL = "postgresql://postgres:12345@localhost:5433/ai_vision"
```
Adjust this string if your port, username, or password differs.

Initialize the table schemas using:
```powershell
$env:PYTHONPATH="."
python -m app.database.init_db
```

---

## 🏃 Running the Application

### 1. Streamlit Web Dashboard
Launch the interactive dashboard to upload media, adjust detection confidence thresholds, and see live results:
```powershell
streamlit run streamlit_app.py
```
Open the application at `http://localhost:8501`.

### 2. Command Line Interface (CLI)
For quick local processing of images/videos:
```powershell
$env:PYTHONPATH="."
python main.py
```
*Enter the target file path when prompted (e.g. `data/videos/Traffic_30sec.mp4`).*

---

## 📈 Model Performance & Validation

Below are the performance metrics and validation charts tracked during training the custom emergency vehicle classification model.

### 📊 Metric Graphs & Performance Metrics

#### 1. Confusion Matrix
The confusion matrix measures classification accuracy. It compares actual labels (Ambulance, Fire Truck, Police Car, Background) against model predictions, highlighting true positives and false detection rates.
![Confusion Matrix](confusion_matrix.png)

<br>

#### 2. Precision-Recall (PR) Curve
Plots precision (exactness) vs. recall (completeness) for bounding box predictions. Higher Area Under Curve (AUC) indicates a model that is both highly accurate and generalizable.
![Precision-Recall Curve](BoxPR_curve.png)

<br>

#### 3. Training & Validation Loss Curves
Tracks Box Loss (bounding box location regression), Class Loss (classification accuracy), and DFL Loss (Distribution Focal Loss) over training epochs. Steady declines in both train and val losses indicate successful convergence.
![Training Results](results.png)

<br>

#### 4. Bounding Box & Label Distributions
Visualizes the shape, center location coordinates, and instance count distributions of labels within the emergency vehicle training dataset.
![Dataset Labels](labels.jpg)

---

## 💡 Algorithmic Highlights

### IoU-based Duplicate Removal & ID Inheritance
When standard vehicles and emergency vehicles are processed simultaneously, the same emergency vehicle can be double-detected. 
1. We compute **Intersection over Union (IoU)** for overlapping bounding boxes.
2. If `IoU > 0.50` between a general detection (e.g., `car`/`truck`) and an emergency vehicle detection (e.g., `ambulance`), the general detection is discarded.
3. The emergency detection inherits the tracking ID of the general vehicle detection to maintain identity tracking over subsequent frames.

### Video-Clock Stopped Vehicle Detection
Instead of system clock timers, we rely on video-clock metrics to support non-real-time processing speeds:
$$\text{Relative Time} = \frac{\text{Current Frame Index}}{\text{Video FPS}}$$
A vehicle is flagged as `STOPPED` if its bounding box center moves less than **10 pixels** over a span of **6.0 seconds** of video time.

---

## 🔮 Future Improvements
* **Active Green Light Override**: Integrate with traffic controller APIs to automatically force green lights along the calculated trajectory of oncoming emergency vehicles.
* **Speed Estimation**: Map camera pixel coordinates to real-world coordinates using a Homography matrix to calculate vehicle velocities and trigger speeding events.

---

### Author
Samyak Rawat | AI/ML Engineer | Thapar Institute of Engineering and Technology
