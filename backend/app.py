from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time
from monitor import HealthMonitor
from healer import AutoHealer
from alerter import Alerter
from predictor import FailurePredictor

app = Flask(__name__)
CORS(app)

monitor = HealthMonitor()
healer = AutoHealer()
alerter = Alerter()
predictor = FailurePredictor()

# ─── Background monitoring loop ──────────────────────────────────
def monitoring_loop():
    while True:
        status = monitor.check_all()
        for service, health in status.items():
            if health['status'] == 'DOWN':
                print(f"[ALERT] {service} is DOWN — attempting auto-heal...")
                healer.heal(service)
                alerter.send_whatsapp(
                    f"🚨 MediOps Alert\n"
                    f"Service: {service}\n"
                    f"Status: DOWN detected\n"
                    f"Action: Auto-healing started..."
                )
        time.sleep(15)  # Check every 15 seconds

# ─── API Routes ───────────────────────────────────────────────────
@app.route('/api/health', methods=['GET'])
def get_health():
    """Returns live health status of all hospital services"""
    status = monitor.check_all()
    return jsonify(status)

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Returns CPU, RAM, Disk metrics"""
    return jsonify(monitor.get_system_metrics())

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Returns alert history from DB"""
    return jsonify(alerter.get_alert_history())

@app.route('/api/predict', methods=['GET'])
def predict_failure():
    """AI prediction — will system fail in next 2 hours?"""
    prediction = predictor.predict()
    return jsonify(prediction)

@app.route('/api/heal/<service>', methods=['POST'])
def manual_heal(service):
    """Manually trigger healing for a service"""
    result = healer.heal(service)
    return jsonify(result)

# ─── Start background monitor thread ─────────────────────────────
if __name__ == '__main__':
    monitor_thread = threading.Thread(target=monitoring_loop, daemon=True)
    monitor_thread.start()
    print("MediOps Backend running on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)
