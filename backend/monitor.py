import psutil
import requests
import datetime

class HealthMonitor:
    def __init__(self):
        # Hospital services to monitor
        self.services = {
            'OPD Server':       'http://localhost:8001/ping',
            'Patient DB':       'http://localhost:8002/ping',
            'Pharmacy System':  'http://localhost:8003/ping',
            'Lab Reports':      'http://localhost:8004/ping',
        }

    def check_service(self, name, url):
        """Ping a service — returns UP or DOWN"""
        try:
            res = requests.get(url, timeout=3)
            if res.status_code == 200:
                return {'status': 'UP', 'response_time': res.elapsed.total_seconds()}
        except Exception:
            pass
        return {'status': 'DOWN', 'response_time': None}

    def check_all(self):
        """Check all hospital services"""
        result = {}
        for name, url in self.services.items():
            result[name] = self.check_service(name, url)
            result[name]['checked_at'] = str(datetime.datetime.now())
        return result

    def get_system_metrics(self):
        """Get CPU, RAM, Disk usage"""
        return {
            'cpu_percent':    psutil.cpu_percent(interval=1),
            'ram_percent':    psutil.virtual_memory().percent,
            'ram_used_gb':    round(psutil.virtual_memory().used / 1e9, 2),
            'disk_percent':   psutil.disk_usage('/').percent,
            'disk_free_gb':   round(psutil.disk_usage('/').free / 1e9, 2),
            'timestamp':      str(datetime.datetime.now()),
            'risk_level':     self._get_risk_level()
        }

    def _get_risk_level(self):
        cpu  = psutil.cpu_percent()
        ram  = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        if cpu > 90 or ram > 90 or disk > 95:
            return 'CRITICAL'
        elif cpu > 70 or ram > 75 or disk > 80:
            return 'WARNING'
        return 'HEALTHY'
