# 🏥 MediOps — Hospital Infrastructure Auto-Healing System

> "Servers fix themselves. Doctors focus on patients."

## 🎯 What it does
MediOps is a DevOps-heavy system that **monitors hospital IT infrastructure 24/7** and automatically fixes issues before they affect patients.

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/mauryashivi199-ui/mediops.git
cd mediops

# 2. Set environment variables
cp .env.example .env
# Edit .env with your Twilio, AWS credentials

# 3. Start everything with Docker
docker-compose up -d

# 4. Open dashboards
# App:        http://localhost:3000
# Grafana:    http://localhost:3001
# Prometheus: http://localhost:9090
```

## 🛠️ Tech Stack
| Layer | Tech |
|-------|------|
| Backend | Python + Flask |
| Frontend | React.js |
| Containers | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Cloud | AWS EC2 + S3 |
| Monitoring | Prometheus + Grafana |
| Alerts | Twilio WhatsApp API |
| Database | PostgreSQL |

## 📁 Project Structure
```
mediops/
├── backend/          # Python Flask API
│   ├── app.py        # Main API server
│   ├── monitor.py    # Health check system
│   ├── healer.py     # Auto-healing logic
│   ├── alerter.py    # WhatsApp + Slack alerts
│   └── predictor.py  # AI failure prediction
├── frontend/         # React Dashboard
├── monitoring/       # Prometheus + Grafana config
├── .github/          # GitHub Actions CI/CD
├── scripts/          # Bash automation scripts
└── docker-compose.yml
```

## 👩‍💻 
- **Shivangi Maurya** — DevOps Engineer (MGIMT Lucknow)
  
