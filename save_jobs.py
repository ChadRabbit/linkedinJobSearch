OUTPUT_FILE = "jobs.txt"


def save_to_txt(jobs):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for job in jobs:
            f.write("====================================\n")
            f.write(f"Company: {job['company']}\n")
            f.write(f"Role: {job['title']}\n")
            f.write(f"Location: {job['location']}\n")
            f.write(f"Link: {job['link']}\n\n")
            f.write(f"Score: {job['score']}\n")
