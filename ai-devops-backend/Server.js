const express = require('express');
const cors = require('cors');
const fs = require('fs');

const app = express();
app.use(cors());
app.use(express.json());

// Load mock data
const logs = JSON.parse(fs.readFileSync('./mock_data/logs.json', 'utf8'));
const tasks = JSON.parse(fs.readFileSync('./mock_data/tasks.json', 'utf8'));
const metrics = JSON.parse(fs.readFileSync('./mock_data/metrics.json', 'utf8'));

// API endpoints
app.get('/logs', (req, res) => {
    res.json(logs);
});

app.get('/tasks', (req, res) => {
    res.json(tasks);
});

app.get('/metrics', (req, res) => {
    res.json(metrics);
});

app.get('/insights', (req, res) => {
    const insights = [];

    const failedCount = logs.filter(l => l.status === "FAILED").length;
    if (failedCount >= 3) {
        insights.push("Multiple build failures detected — Check memory usage or dependencies.");
    }

    const now = new Date();
    tasks.forEach(task => {
        const diffDays = Math.floor((now - new Date(task.lastUpdated)) / (1000 * 60 * 60 * 24));
        if (diffDays > 3) {
            insights.push(`Ticket ${task.id} is idle for ${diffDays} days — consider reassignment.`);
        }
    });

    if (metrics.cpu.some(usage => usage > 85)) {
        insights.push("High CPU usage detected — consider scaling up.");
    }

    res.json({ insights });
});

// Start server
const PORT = 5000;
app.listen(PORT, () => console.log(`Backend running on port ${PORT}`));
