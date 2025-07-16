import os
import requests
import psutil
import platform
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# === CONFIG ===
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_temperature():
    try:
        output = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
        return output.strip().replace("temp=", "")
    except Exception:
        return "N/A"

def get_uptime():
    return subprocess.check_output("uptime -p", shell=True).decode().strip()

def get_metrics():
    cpu_percent = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    temp = get_temperature()
    uptime = get_uptime()

    metrics = f"""📊 *Raspberry Pi Metrics - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
🌡 Température : `{temp}` \n
🖥 CPU usage : `{cpu_percent}%` \n
🧠 RAM usage : `{ram.percent}%` ({round(ram.used / 1024**2)} MB used) \n
💽 Disk usage : `{disk.percent}%` ({round(disk.used / 1024**3)} GB used) \n
⏱ Uptime : `{uptime}` \n
📟 OS : `{platform.system()} {platform.release()}`
"""
    return metrics

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=data)
        if not response.ok:
            print("Erreur Telegram:", response.text)
    except Exception as e:
        print("Erreur d’envoi:", e)

if __name__ == "__main__":
    message = get_metrics()
    send_telegram_message(message)
