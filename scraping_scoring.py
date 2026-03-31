import random
import time

TOP_COMPANIES = {
    "google", "amazon", "microsoft", "apple", "meta",
    "netflix", "adobe", "salesforce", "uber", "airbnb",
    "stripe", "atlassian", "linkedin", "twitter", "x",
    "flipkart", "swiggy", "zomato", "razorpay", "cred",
    "phonepe", "paytm", "ola", "meesho", "groww",
    "zerodha", "nykaa", "freshworks", "postman",
    "intuit", "oracle", "sap", "cisco", "vmware",
    "nvidia", "qualcomm", "intel", "amd",
    "goldman sachs", "jpmorgan", "morgan stanley",
    "de shaw", "tower research", "worldquant",
    "optiver", "blackrock", "paypal", "booking.com",
    "expedia", "agoda", "bytedance", "tiktok"
}


def scroll_jobs_list(page):
    jobs = page.locator("div.job-card-list__entity-lockup")

    # wait for jobs to load
    jobs.first.wait_for(timeout=10000)

    # move mouse to first job (so scrolling happens on left side of page)
    box = jobs.first.bounding_box()
    if box:
        page.mouse.move(
            box["x"] + box["width"] / 2,
            box["y"] + box["height"] / 2
        )

    prev_count = 0
    stable_rounds = 0
    for _ in range(10):
        page.mouse.wheel(0, 1200)
        time.sleep(random.uniform(1.0, 2.0))  # random sleep to mimic human behavior
        curr_count = jobs.count()
        print("Loaded jobs:", curr_count)

        if curr_count == prev_count:
            stable_rounds += 1
        else:
            stable_rounds = 0

        # only stop if stable multiple times (no new jobs found)
        if stable_rounds >= 3:
            break

        if curr_count >= 25:
            break

        prev_count = curr_count


def scrape_page(page):
    jobs = page.locator("div.job-card-list__entity-lockup")
    count = jobs.count()

    results = []

    for i in range(count):
        job = jobs.nth(i)

        try:
            title_el = job.locator("a strong").first
            link_el = job.locator("a").first  # for link
            raw_title = title_el.text_content()
            title = raw_title.strip() if raw_title else ""
            link = link_el.get_attribute("href")
            company_el = job.locator("div.artdeco-entity-lockup__subtitle span").first
            location_el = job.locator("div.artdeco-entity-lockup__caption span").first

            company = company_el.text_content()
            location = location_el.text_content()

            company = company.strip() if company else ""
            location = location.strip() if location else ""
            print(f"Job {i + 1}")
            print("Title:", title)
            print("Company:", company)
            print("Location:", location)
            print("-" * 50)

            full_link = "https://www.linkedin.com" + link if link else None
            print("Link:", full_link)

            if not full_link:
                continue

            job_data = {
                "title": title,
                "company": company,
                "location": location,
                "link": full_link
            }

            job_data["score"] = score_job(job_data)

            results.append(job_data)


        except:
            continue

    return results


def normalize(text):
    return text.strip().lower() if text else ""


def deduplicate_jobs(jobs):
    seen = set()
    unique_jobs = []

    for job in jobs:
        company = normalize(job["company"])
        title = normalize(job["title"])
        location = normalize(job["location"])

        key = (company, title, location)
        if "Apple" in job["company"]:
            print(job)
            print(key)

        if key in seen:
            continue

        seen.add(key)
        unique_jobs.append(job)

    return unique_jobs


def score_job(job):
    score = 0

    title = job["title"].lower()
    location = job["location"].lower()
    company = job["company"].lower()

    #  Role scoring
    if "intern" in title:
        score += 5
    if "software engineer" in title:
        score += 4
    if "sde" in title:
        score += 4
    if "developer" in title:
        score += 3
    if "frontend" in title or "backend" in title:
        score += 3

    #  Penalize senior roles
    if "senior" in title or "sr." in title:
        score -= 30
    if "lead" in title or "manager" in title:
        score -= 30

    #  Location preference (personal)
    if "bengaluru" in location:
        score += 5
    elif "mumbai" in location:
        score += 4
    elif "gurgaon" in location or "delhi" in location:
        score += 3
    elif "hyderabad" in location:
        score += 2

    # 🔥 Company boost (BIG signal)
    for top in TOP_COMPANIES:
        if top in company:
            score += 30
            break

    return score
