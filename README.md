
# Traffic-Based Route Guidance System (TBRGS)

**COS30019 – Intelligent Systems Assignment 2B**  
Team ID: Group 3

## 🧠 Project Overview

This project implements a **Traffic-Based Route Guidance System (TBRGS)** that uses machine learning models to forecast traffic volumes and estimate optimal travel paths through the City of Boroondara. By combining predictive modeling with graph search algorithms, the system dynamically guides users through the most efficient routes based on expected traffic conditions.

This system builds upon the foundational work from Assignment 2A and extends it with:
- Multiple time-series machine learning models (LSTM, GRU, and a third model)
- Dynamic prediction of future traffic volume
- Travel time estimation based on predicted traffic
- A top-k shortest path route finder
- A user-friendly graphical interface for real-time interaction

---

## 📁 Project Structure

```
TBRGS/
├── data/
│   ├── raw/
│   │   └── boroondara_oct2006.csv
│   ├── processed/
│   │   └── traffic_processed.csv
│   └── external/                    # Any additional datasets (if used in research)
│
├── notebooks/                      # For Jupyter notebooks (data exploration, testing models)
│   ├── EDA.ipynb                   # Exploratory Data Analysis
│   ├── LSTM_Model.ipynb
│   ├── GRU_Model.ipynb
│   └── Other_Model.ipynb     ,     # 3rd ML model (e.g., Random Forest, ARIMA, Transformer)
│
├── models/                         # Trained models and training scripts
│   ├── lstm_model.py
│   ├── gru_model.py
│   ├── other_model.py
│   └── saved_models/
│       ├── lstm.pth
│       ├── gru.pth
│       └── other_model.pkl
│
├── src/                            # Core application logic
│   ├── __init__.py
│   ├── data_processing.py         # Clean, normalize, and prepare data
│   ├── prediction_engine.py       # Load models and predict future traffic volumes
│   ├── travel_time_estimator.py   # Convert volume to travel time
│   ├── route_finder.py            # Search top-k paths using graph search
│   └── config.py                  # Default parameters/settings
│
├── gui/                            # User interface
│   ├── main_gui.py                # Entry point for GUI
│   └── gui_utils.py               # GUI logic helpers (tkinter, PyQt, etc.)
│
├── tests/                          # Automated or manual test cases
│   ├── test_data_processing.py
│   ├── test_model_prediction.py
│   ├── test_travel_time_estimator.py
│   └── test_route_finder.py
│
├── report/
│   ├── TeamID.pdf                 # Final report
│   └── figures/                   # Graphs, model comparisons, results screenshots
│
├── config.json                    # JSON for storing user/default configs
├── README.md                      # Project overview, how to run the system
├── requirements.txt               # Python dependencies
└── run.py                         # Main entry script for running the entire system

```

---

## 📊 Machine Learning Models

We implemented and compared the following time-series models:

- **LSTM (Long Short-Term Memory):** RNN variant effective for sequence prediction.
- **GRU (Gated Recurrent Unit):** Lightweight alternative to LSTM with fewer parameters.
- **[Third Model, e.g., Random Forest Regressor or Transformer]:** Chosen for baseline or hybrid performance.

Each model was trained on traffic volume data recorded from sensors across Boroondara in October 2006, predicting volume at 15-minute intervals for future times.

---

## 🧮 How It Works

### 1. **Data Preprocessing**
   - Load and clean time-series traffic sensor data
   - Normalize and reshape for training ML models

### 2. **Traffic Forecasting**
   - Train LSTM, GRU, and another model on historical data
   - Predict traffic volume for user-selected future times

### 3. **Travel Time Estimation**
   - Translate predicted volume into travel time using a regression-based mapping formula

### 4. **Route Finding**
   - Construct a graph where nodes = intersections and edges = road segments
   - Use Dijkstra’s algorithm or A* to calculate **top-k shortest paths** by predicted travel time

### 5. **Graphical User Interface**
   - Users select source, destination, and future time
   - GUI displays top-k recommended paths with estimated travel times and visual overlays

---

## 🚀 Getting Started

### Step 1: Clone the Repository
```bash
git clone 
cd TBRGS
```

### Step 2: Install Dependencies
Ensure you have Python 3.9+ installed, then:
Make an Anconda environment and install with followings
```bash
pip install -r requirements.txt
```

### Step 3: Launch the App
```bash
python run.py
```

This will open the GUI for route prediction and display.

---

## 🧪 Testing

To run all unit and integration tests:
```bash
pytest tests/
```

---

## 📷 Sample Screenshots

> Add screenshots of:
> - Traffic volume prediction graph
> - Route visualization with top-k paths
> - GUI home screen

---

## 👨‍💻 Team Members

- Yasiru Lokesha  
- Prawud Rathnayake 
- 
- 

---

## 📄 Final Report

All technical documentation, architecture diagrams, and evaluation metrics are available in:  
📁 `report/TeamID_Report.pdf`

---

## 📌 Notes

- The dataset used is **City of Boroondara – Traffic Sensor Data (October 2006)**.
- The prediction models rely solely on the provided historical data without external sources.
- GUI developed using [Tkinter / PyQt] – supports real-time input and route display.
- Graph-based pathfinding uses NetworkX.

---

## 📦 Dependencies

Here are the main Python libraries used:

```text
numpy
pandas
scikit-learn
matplotlib
seaborn
tensorflow
keras
torch
networkx
tkinter
PyQt5
```

All dependencies can be installed with:
```bash
pip install -r requirements.txt
```

---

## 📜 License

This project is submitted for academic purposes only for COS30019.  
All content is original and not intended for commercial or distribution use.

---
