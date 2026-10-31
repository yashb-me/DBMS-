# 🛡️ Student Welfare & Attendance Management System
**Course Project:** Database Systems (BACSE202) — VIT Vellore  
**Tech Stack:** Pure Python (Streamlit Flat Cream UI) + SQLite 3 (WAL Engine)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-SQLite%203%20(WAL)-orange.svg)](https://www.sqlite.org/)

A proactive, early-warning student welfare platform implemented directly at the database layer. Rather than treating attendance tracking as mundane record-keeping, this system uses **SQLite Event Triggers, B+ Tree Indexes, Materialized Views, and Transaction Savepoints** to detect academic distress, monitor chronic absence streaks, and automate welfare alerts in real time.

---

## 🎪 Core Database Features & Live 3D Visualizers

| Tab / View | Database Topic | Real-Time 3D Visualization |
|---|---|---|
| **🔴 Live Attendance & Alerts** | `AFTER INSERT TRIGGER`, Atomic Inserts | **3D Trigger Pipeline**: Incoming attendance record moves through the trigger chamber and autonomously ejects a critical alert. |
| **⚡ Query Performance** | B+ Tree Composite Indexes, `EXPLAIN QUERY PLAN` | **Access Path Comparator**: Race between 3-hop B+ Tree index traversal ($O(\log N)$) vs crawling sequential table scan ($O(N)$) over 9,000 rows. |
| **⏱️ Attendance Rollback & History** | ACID Atomicity, `SAVEPOINT`, `ROLLBACK TO` | **3D Transaction Stack**: Intermediate savepoint checkpoints where accidental corrupted batch frames are physically ejected from the memory stack. |
| **📊 Department Analytics** | Relational Views, Window Functions, Materialization | **Incremental Materialization Router**: Incoming attendance packets route directly into departmental accumulator buckets without rescanning all 9,000 rows. |
| **📐 Database Architecture** | 1NF, 2NF, 3NF Normalization, Constraints | **Schema & Normalization Explorer**: Interactive column inspector, foreign key relationships, and functional dependency proof. |

---

## 🗄️ Database Architecture

* **Database Engine**: SQLite 3 with Write-Ahead Logging (`PRAGMA journal_mode=WAL;`)
* **Foreign Key Enforcement**: `PRAGMA foreign_keys = ON;`
* **Concurrency Handling**: `PRAGMA busy_timeout = 5000;`
* **Pre-seeded Dataset**: 50 students, 12 faculty, 12 subjects, and **9,000+ verified attendance records**.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PHYSICAL STORAGE LAYER                          │
│  • attendance.db (Write-Ahead Logging: PRAGMA journal_mode=WAL;)       │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
        ┌────────────────────────────┼───────────────────────────┐
        ▼                            ▼                           ▼
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│   CORE TABLES    │       │     TRIGGERS     │       │      VIEWS       │
│ • students (50)  │       │ • auto_streak    │       │ • student_risk   │
│ • attendance(9k) │       │ • refresh_mv     │       │   (Window Func)  │
│ • alerts (12)    │       │ • audit_ack      │       │ • alert_details  │
│ • subjects (12)  │       │ • auto_low_att   │       │ • weekly_summary │
│ • faculty (12)   │       └──────────────────┘       └──────────────────┘
│ • warden (2)     │                 │                           │
│ • audit_log      │                 ▼                           │
│ • hostel_logs    │       ┌──────────────────┐                  │
│ • lms_activity   │       │   MAT. TABLES    │                  │
└──────────────────┘       │ • mv_dept_att    │◄─────────────────┘
                           │ • mv_risk_trend  │
                           └──────────────────┘
```

---

## 🚀 Running Locally

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/student-welfare-attendance-dbms.git
cd student-welfare-attendance-dbms
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the dashboard
```bash
python3 -m streamlit run dashboard.py
```
Open **`http://localhost:8501`** in your browser.

---

## ☁️ Deploying Live on Streamlit Cloud (Free & Serverless)

1. Push this repository to **GitHub**.
2. Go to **[share.streamlit.io](https://share.streamlit.io/)** and sign in with GitHub.
3. Click **"New app"**.
4. Select your repository, set branch to `main`, and main file path to:
   ```
   dashboard.py
   ```
5. Click **"Deploy"**!  
   Your project will be live with a shareable URL like:
   `https://<your-username>-student-welfare-dbms.streamlit.app`

---

## 👥 4-Member Team Presentation Guide
For the complete viva presentation manual and query-by-query walkthrough, see:
📖 **[`instructions.md`](instructions.md)**

---

*VIT Vellore · Database Systems (BACSE202) Project*
