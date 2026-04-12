import os
import requests
import datetime
from twilio.rest import Client

class Alerter:
    def __init__(self):
        self.twilio = Client(os.getenv('TWILIO_SID'), os.getenv('TWILIO_TOKEN'))
        self.from_phone   = os.getenv('TWILIO_PHONE')
        self.alert_phone  = os.getenv('ALERT_PHONE')
        self.slack_webhook = os.getenv('SLACK_WEBHOOK')
        self.alert_history = []

    def send_whatsapp(self, message):
        """Send WhatsApp alert via Twilio"""
        try:
            self.twilio.messages.create(
                body=message,
                from_=self.from_phone,
                to=self.alert_phone
            )
            self._log_alert('WhatsApp', message, True)
        except Exception as e:
            self._log_alert('WhatsApp', message, False, str(e))

    def send_slack(self, message):
        """Send Slack alert via webhook"""
        try:
            requests.post(self.slack_webhook, json={'text': message}, timeout=5)
            self._log_alert('Slack', message, True)
        except Exception as e:
            self._log_alert('Slack', message, False, str(e))

    def send_critical_alert(self, service, issue, action_taken):
        """Send full critical alert to all channels"""
        msg = (
            f"🚨 *MediOps Critical Alert*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🏥 Service: {service}\n"
            f"❌ Issue: {issue}\n"
            f"⚡ Action: {action_taken}\n"
            f"🕐 Time: {datetime.datetime.now().strftime('%H:%M:%S')}\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        self.send_whatsapp(msg)
        self.send_slack(msg)

    def _log_alert(self, channel, message, success, error=None):
        self.alert_history.append({
            'channel':   channel,
            'message':   message[:100],
            'success':   success,
            'error':     error,
            'timestamp': str(datetime.datetime.now())
        })

    def get_alert_history(self):
        return self.alert_history[-50:]  # Last 50 alerts
