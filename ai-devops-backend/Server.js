const express = require('express');
const cors = require('cors');
const fs = require('fs');
const { exec } = require('child_process');
const axios = require("axios");

const app = express();
app.use(cors());
app.use(express.json());

// Run Python script to generate fresh mock data before loading
exec('python ./mock_data/generate_data.py', (err, stdout, stderr) => {
    if (err) {
        console.error(`❌ Error generating mock data: ${err.message}`);
        return;
    }
    if (stderr) {
        console.error(`⚠️ stderr: ${stderr}`);
    }
    console.log(`✅ Mock data generated: ${stdout}`);
});

// Helper function to reload JSON after generation
function loadData() {
    return {
        logs: JSON.parse(fs.readFileSync('./mock_data/logs.json', 'utf8')),
        tasks: JSON.parse(fs.readFileSync('./mock_data/tasks.json', 'utf8')),
        metrics: JSON.parse(fs.readFileSync('./mock_data/metrics.json', 'utf8')),
    };
}

// API endpoints
app.get('/logs', (req, res) => {
    const { logs } = loadData();
    res.json(logs);
});

app.get('/tasks', (req, res) => {
    const { tasks } = loadData();
    res.json(tasks);
});

app.get('/metrics', (req, res) => {
    const { metrics } = loadData();
    res.json(metrics);
});

// Insights endpoint -> calls Flask model
app.get('/insights', async (req, res) => {
    const { logs, tasks, metrics } = loadData();

    try {
        const response = await axios.post("http://127.0.0.1:5001/insights", {
            logs,
            tasks,
            metrics
        });
        res.json(response.data);
    } catch (error) {
        console.error("❌ Error fetching insights:", error.message);
        res.status(500).json({ error: "Failed to fetch insights from ML model" });
    }
});

// Start server
const PORT = 5000;
app.listen(PORT, () => console.log(`🚀 Backend running on port ${PORT}`));
