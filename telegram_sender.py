import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)


def send_jobs_smart(jobs, max_chars=3800):
    msg = "🔥 Top Job Alerts\n\n"

    for i, job in enumerate(jobs, 1):
        job_block = ""
        job_block += f"{i}. {job['title']} ({job['score']})\n"
        job_block += f"{job['company']} | {job['location']}\n"
        job_block += f"{job['link']}\n\n"

        # 🔥 if adding this job exceeds limit → send current msg
        if len(msg) + len(job_block) > max_chars:
            send_telegram(msg)
            time.sleep(1)
            # start new message
            msg = "🔥 Job Alerts (cont.)\n\n"

        msg += job_block

    # send remaining
    if msg.strip():
        send_telegram(msg)
