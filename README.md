# AI-DevOps Monitoring Prototype

This project is a prototype for ’ AI-driven DevOps monitoring system**.  
It integrates an **ML anomaly detection model**, a **Flask backend API**, and a **React + Tailwind frontend dashboard** to provide insights into **logs, tasks, and system metrics in real time**.

---
**Note:** The entire project is currently in the **`dev` branch**, not the `main` branch.  
After cloning, make sure to switch to the `dev` branch:
##  Project Structure
ai-devops/
│
├─ backend/
│ ├─ mock_data/
│ │ ├─ generate_data.py # Generates synthetic logs, tasks, and metrics
│ │ ├─ logs.json # Stores generated log data
│ │ ├─ tasks.json # Stores generated task data
│ │ └─ metrics.json # Stores generated metrics
│ │
│ ├─ models/
│ │ ├─ synthetic_logs.csv
│ │ ├─ synthetic_metrics.csv
│ │ ├─ synthetic_tasks.csv
│ │ ├─ isolation_model.py # Trains Isolation Forest model
│ │ └─ trained_model.pkl # Saved anomaly detection model
│ │
│ ├─ app.py # Flask API (loads data + model + serves predictions)
│ ├─ server.js # Runs generate_data.py via Node.js
│
├─ frontend/
│ ├─ src/
│ │ ├─ App.js
│ │ ├─ App.css
│ │ ├─ index.js
│ │ ├─ index.css
│ │ ├─ components/
│ │ │ ├─ Logs.js
│ │ │ ├─ Tasks.js
│ │ │ ├─ Metrics.js
│ │ │ └─ Insights.js
│ │ ├─ reportWebVitals.js
│ │ └─ setupTests.js
│ ├─ package.json
│ ├─ tailwind.config.js
│ └─ README.md (this file)

yaml
Copy
Edit

---

 Tech Stack
- **Backend**: Python, Flask, Flask-CORS, Pandas, Scikit-learn, Joblib  
- **Frontend**: React.js, Tailwind CSS  
- **Utilities**: Node.js (to run Python script for synthetic data generation)  

---

 Setup & Run  

 Clone Repo  
```bash
git clone https://github.com/<your-username>/ai-devops.git
cd ai-devops
Backend Setup
Navigate to the backend folder and install dependencies:

bash
Copy
Edit
cd backend

pip install flask
pip install flask-cors
pip install pandas
pip install scikit-learn
pip install joblib
(Python built-in libraries like json, os, and datetime do not need installation.)

Run the Flask API:

bash
Copy
Edit
python app.py
 Run Data Generator
Open a new terminal and start the data generator:

bash
Copy
Edit
node server.js
 Frontend Setup
In another terminal, set up and start the React app:

bash
Copy
Edit
cd frontend
npm install
npm start
 Usage
Open the React dashboard in your browser (http://localhost:3000).

Logs, tasks, and metrics will be displayed in real time.

Anomaly detection insights come from the trained Isolation Forest model
