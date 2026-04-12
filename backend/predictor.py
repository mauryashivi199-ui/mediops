import psutil
import datetime

class FailurePredictor:
    """
    Simple rule-based AI predictor.
    In real version: trained ML model on historical metrics.
    """

    def predict(self):
        cpu    = psutil.cpu_percent(interval=1)
        ram    = psutil.virtual_memory().percent
        disk   = psutil.disk_usage('/').percent

        risk_score = 0
        warnings = []

        # CPU rules
        if cpu > 85:
            risk_score += 40
            warnings.append(f"CPU at {cpu}% — very high load")
        elif cpu > 70:
            risk_score += 20
            warnings.append(f"CPU at {cpu}% — elevated")

        # RAM rules
        if ram > 90:
            risk_score += 40
            warnings.append(f"RAM at {ram}% — critical")
        elif ram > 75:
            risk_score += 20
            warnings.append(f"RAM at {ram}% — elevated")

        # Disk rules
        if disk > 95:
            risk_score += 30
            warnings.append(f"Disk at {disk}% — almost full")
        elif disk > 80:
            risk_score += 10
            warnings.append(f"Disk at {disk}% — filling up")

        # Determine risk level
        if risk_score >= 60:
            level = 'HIGH'
            recommendation = 'Restart services now. Failure likely within 2 hours.'
        elif risk_score >= 30:
            level = 'MEDIUM'
            recommendation = 'Monitor closely. Consider freeing up resources.'
        else:
            level = 'LOW'
            recommendation = 'System is healthy. No action needed.'

        return {
            'risk_score':     risk_score,
            'risk_level':     level,
            'warnings':       warnings,
            'recommendation': recommendation,
            'predicted_at':   str(datetime.datetime.now()),
            'metrics': {
                'cpu': cpu,
                'ram': ram,
                'disk': disk
            }
        }
