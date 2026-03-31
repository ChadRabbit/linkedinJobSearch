# 🚀 LinkedIn Job Automation System

### A smart job scraping and filtering system that automates LinkedIn job search and delivers only relevant opportunities directly to Telegram.
### This project is for educational and learning purposes only.
---

## 📌 Overview

Manually browsing job listings can be repetitive and inefficient.

This project solves that by:
- Scraping LinkedIn job listings using Playwright
- Cleaning and deduplicating results
- Ranking jobs based on relevance (role, company, location)
- Filtering out low-quality or irrelevant roles
- Sending top jobs directly to Telegram

---

## ⚙️ Features

- 🔍 Automated job scraping (LinkedIn)
- 🧹 Deduplication using company + role + location
- ⭐ Heuristic-based job scoring system
- 🏢 Company-based prioritization (top tech + product companies)
- 📍 Location-based ranking (Bengaluru > Mumbai > NCR > Hyderabad)
- 📩 Telegram alerts with clean formatting
- 📦 Smart batching (avoids message limits)
- 💾 File export for debugging (`jobs.txt`) 

---

## 🧠 Scoring Logic

Jobs are ranked using a custom scoring system:

- Role relevance (SDE, Intern, Developer)
- Company quality (Top tech companies get a boost)
- Location preference
- Penalization for senior roles

This avoids unnecessary dependence on AI and keeps the system efficient.

---

## 🚀 Setup

### 1. Clone the repository

### 2. Install the dependancies

```bash
pip install -r requirements.txt
```

### 3. Add the Telegram Token and Chat Id
Create a `.env` file from the example and set your key.

### 4. Save your LinkedIn sessions
```bash
python save_session.py
```

### 5. Run the Scheduler class
```bash
python scheduler.py
```
