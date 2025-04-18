# 🌌 AstroSage

Explore the universe of exoplanets with **AstroSage** — an interactive dashboard and public API built on real NASA exoplanet data. Compare distant worlds, evaluate their habitability, and discover new planetary systems like never before.

---

## 🚀 What is AstroSage?

AstroSage is a full-stack application that makes space data accessible and meaningful through:
- 🌍 A custom **Habitability Score** (0 to 1)
- 📈 Interactive **visualizations** built with Plotly
- 🌐 A RESTful **API** to query planets, habitability, and discovery timelines
- 🧠 A tiny ML model predicting a planet's habitability potential

Built for science education, data exploration, and space enthusiasts.

---

## 🔬 Key Features

### 🛰️ Dashboard
- Real-time stats on total and habitable exoplanets
- Discovery method charts
- Featured planet showcase

### 🌍 Habitability Explorer
- List of potentially habitable worlds
- Interactive scatter plots: Habitability vs Distance, Size vs Temp
- Click to view detailed planet profiles

### 🧪 Planet Comparison Tool
- Compare two planets side-by-side
- Size, distance, temp, habitability score comparison

### 🕒 Discovery Timeline
- Visualize exoplanet discoveries over time
- Timeline chart + chronological listing

### 🤖 ML Habitability Prediction
- Predict habitability using radius, temp, and distance
- Model: Random Forest Classifier (basic, educational)

---

## 🔧 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/exoplanet/<name>` | Get data on a specific exoplanet |
| `/api/exoplanets/habitable` | List potentially habitable planets |
| `/api/exoplanets/discovered/last-year` | Get recent discoveries |
| `/api/dashboard/stats` | Get real-time stats |

> Bonus: All major sections have visual endpoints too (e.g., `/visualization`).

---

## 💻 How to Run It Locally

### 1. Clone the Repo
```bash
git clone https://github.com/Muneer-ul-hassan/astrosage.git
cd astrosage
2. Install Requirements
bash
Copy
Edit
pip install -r requirements.txt
3. Run the App
bash
Copy
Edit
python app.py
Server runs at http://127.0.0.1:5000

📽️ Demo Video
🎥 Watch the video walkthrough here (Link coming soon — update before submission!)

📜 License
This project is open-source under the MIT License.

🛰️ Author
Built with Python, Flask, Plotly, and cosmic curiosity 🌌
@Muneer-ul-hassan
Discord/X: @noob_.masterop
