# CO2 Sequestration Optimization Tool

## 📌 Project Overview
This project is a Python-based Streamlit web application designed to assist field operators in optimizing CO₂ injection parameters for depleted reservoirs.

The application integrates Vertical Flow Performance (VFP) tables exported from reservoir simulators such as ECLIPSE 300 and provides real-time decision support for injection operations.

This tool falls under the concept of a **Digital Oilfield / Energy AI system**, enabling faster and more informed engineering decisions.

---

## 🎯 Key Features

### 1. VFP Table Integration
- Upload VFP data in CSV or ECLIPSE `.INC` format
- Parse and convert simulation output into structured data
- Display pressure-matched lookup tables

### 2. Real-Time Injection Dashboard
Operators can input:
- Tubing Head Pressure (THP)
- Injection Rate
- Bottomhole Temperature
- Water-Gas Ratio (WGR)

The system calculates the corresponding Bottomhole Flowing Pressure (BHFP).

---

### 3. Optimization Engine
- Uses **SciPy interpolation and optimization**
- Recommends optimal injection rate for a target BHFP
- Helps maintain safe and efficient injection conditions

---

### 4. Interactive Visualization
- Plot VFP curves (Rate vs BHFP)
- Display multiple THP curves
- Highlight current operating point
- Sensitivity analysis charts

---

### 5. Decision Support System
Color-coded system:
- 🟢 **Green** → Optimal operation
- 🟡 **Yellow** → Caution
- 🔴 **Red** → Out of range

Provides actionable recommendations for operators.

---

### 6. Export Functionality
- Export results as CSV
- Generate PDF reports for field use

---

## 🧠 Technologies Used

| Technology | Purpose |
|------------|--------|
| Python 3.10+ | Core language |
| Streamlit | Web interface |
| Pandas | Data handling |
| NumPy | Numerical operations |
| SciPy | Interpolation & optimization |
| Plotly | Visualization |
| FPDF | PDF generation |

---

## 📁 Project Structure


co2_optimizer/
├── app.py # Main Streamlit app
├── modules/
│ ├── vfp_parser.py # VFP file parsing
│ ├── interpolator.py # Interpolation logic
│ ├── optimizer.py # Optimization engine
│ ├── visualizer.py # Plotly charts
│ └── exporter.py # Export functions
├── data/
│ ├── sample_vfp.csv # Sample dataset
│ └── sample_vfp.inc # Sample Eclipse file
├── requirements.txt
└── README.md


---

## ⚙️ Installation Guide

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/co2_optimizer.git
cd co2_optimizer
2. Create Virtual Environment
python3 -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
3. Install Dependencies
pip install -r requirements.txt
▶️ Running the Application
streamlit run app.py

The app will open automatically in your browser.

📊 Data Format
CSV Format
THP,Rate,BHFP
100,200,300
ECLIPSE .INC Format (Simplified)
-- THP
50 100 150 200 /

-- RATE
100 200 300 400 /

-- BHFP
200 250 300 350
220 270 320 370 /
🚀 Future Improvements

Support full ECLIPSE .DATA file parsing

Machine learning prediction models

Monte Carlo simulation for uncertainty

Integration with Django backend

Real-time streaming data support

Multi-well optimization

🌍 Use Case

This application is designed for:

Reservoir engineers

Production engineers

Field operators

Energy researchers

🤝 Contribution

Contributions are welcome!

Fork the repo

Create a new branch

Commit your changes

Push to your branch

Open a Pull Request

📄 License

This project is for educational and research purposes.

👨‍💻 Author

Leonard Emelieze
Full-Stack Developer | Geoscientist | Digital Energy Enthusiast

⭐ Acknowledgment

Inspired by digital transformation in the energy sector and real-time decision support systems in reservoir engineering.


