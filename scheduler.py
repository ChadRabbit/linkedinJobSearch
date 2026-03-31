"""
Main Script to scrape LinkedIn jobs, score them, and send top alerts to Telegram.

This script:


Author: Saransh Mehra
"""

from playwright.sync_api import sync_playwright
import time
import random
from dotenv import load_dotenv

from save_jobs import save_to_txt
from scraping_scoring import scrape_page, deduplicate_jobs, scroll_jobs_list
from telegram_sender import send_jobs_smart

load_dotenv()
# ================= CONFIG =================
BASE_URL = "https://www.linkedin.com/jobs/search/?keywords=Software%20Engineer&location=Bengaluru%2C%20Karnataka%2C%20India&f_WT=1%2C3%2C2&f_TPR=a1774451488-&distance=25&sortBy=R"
PAGES = 5  # how many pages to scrape (Almost 25 jobs per page)


# ---------- MAIN ----------

def main():
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir="linkedin_profile",
            headless=False
        )

        page = context.new_page()

        all_jobs = []

        for page_num in range(PAGES):
            start = page_num * 25
            url = BASE_URL + f"&start={start}"

            print(f"\nScraping page {page_num + 1}")

            page.goto(url)
            time.sleep(10)

            scroll_jobs_list(page)

            jobs = scrape_page(page)

            print(f"Jobs found on page: {len(jobs)}")

            all_jobs.extend(jobs)

            time.sleep(random.uniform(2, 4))

        print(f"\nTotal jobs collected: {len(all_jobs)}")

        unique_jobs = deduplicate_jobs(all_jobs)
        unique_jobs.sort(key=lambda x: x["score"], reverse=True)  # Sort by score before saving/sending
        save_to_txt(unique_jobs)
        print(f"After deduplication: {len(unique_jobs)}")
        top_jobs = unique_jobs[:30]
        save_to_txt(top_jobs)
        send_jobs_smart(top_jobs)


if __name__ == "__main__":
    main()
