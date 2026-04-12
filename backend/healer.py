import subprocess
import datetime
import time

class AutoHealer:
    def __init__(self):
        # Maps service name to its Docker container name
        self.container_map = {
            'OPD Server':      'hospital-opd',
            'Patient DB':      'hospital-db',
            'Pharmacy System': 'hospital-pharmacy',
            'Lab Reports':     'hospital-lab',
        }
        self.heal_log = []

    def heal(self, service_name):
        """Auto-restart a failed Docker container"""
        container = self.container_map.get(service_name)
        if not container:
            return {'success': False, 'message': f'Unknown service: {service_name}'}

        start_time = time.time()
        try:
            # Step 1: Stop the container
            subprocess.run(['docker', 'stop', container], capture_output=True, timeout=15)
            time.sleep(2)

            # Step 2: Restart it
            result = subprocess.run(
                ['docker', 'start', container],
                capture_output=True, text=True, timeout=30
            )

            elapsed = round(time.time() - start_time, 1)

            log_entry = {
                'service':    service_name,
                'action':     'auto-restart',
                'success':    result.returncode == 0,
                'time_taken': f'{elapsed}s',
                'timestamp':  str(datetime.datetime.now()),
            }
            self.heal_log.append(log_entry)

            return {
                'success':    result.returncode == 0,
                'message':    f'✅ {service_name} restarted in {elapsed}s',
                'time_taken': elapsed
            }

        except Exception as e:
            return {'success': False, 'message': str(e)}

    def restore_from_backup(self, service_name):
        """Restore DB from AWS S3 backup"""
        try:
            subprocess.run([
                'aws', 's3', 'cp',
                's3://mediops-backups/latest.dump',
                '/tmp/restore.dump'
            ], check=True)

            subprocess.run([
                'pg_restore', '-d', 'mediops', '/tmp/restore.dump'
            ], check=True)

            return {'success': True, 'message': '✅ DB restored from S3 backup'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    def get_heal_log(self):
        return self.heal_log
