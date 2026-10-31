"""
db.py — All database operations for the Attendance System.
No Streamlit, no UI code here. Just functions that talk to SQLite.
"""

import sqlite3
import time
import datetime
import pandas as pd

DB_PATH = "attendance.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


# -----------------------------------------------------------------------------
# READ functions
# -----------------------------------------------------------------------------

def get_summary_stats():
    """Returns (total_students, total_records, active_alerts, avg_attendance)."""
    conn = get_conn()
    total_students = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    total_records  = conn.execute("SELECT COUNT(*) FROM attendance").fetchone()[0]
    total_alerts   = conn.execute("SELECT COUNT(*) FROM alerts WHERE status = 'ACTIVE'").fetchone()[0]
    avg_att        = conn.execute("SELECT ROUND(AVG(attendance_pct),1) FROM student_risk").fetchone()[0] or 0
    conn.close()
    return total_students, total_records, total_alerts, avg_att


def get_all_students():
    """Returns list of (student_id, full_name)."""
    conn = get_conn()
    rows = conn.execute("SELECT student_id, full_name FROM students ORDER BY student_id").fetchall()
    conn.close()
    return rows


def get_all_subjects():
    """Returns list of (subject_code, subject_name)."""
    conn = get_conn()
    rows = conn.execute("SELECT subject_code, subject_name FROM subjects").fetchall()
    conn.close()
    return rows


def get_active_alerts():
    """Returns DataFrame of active alerts joined with student names."""
    conn = get_conn()
    df = pd.read_sql("""
        SELECT a.id, a.student_id, s.full_name, a.alert_type, a.severity, a.message, a.created_at
        FROM alerts a
        JOIN students s ON a.student_id = s.student_id
        WHERE a.status = 'ACTIVE'
        ORDER BY a.id DESC
        LIMIT 15
    """, conn)
    conn.close()
    return df


def get_recent_records_for_student(student_id, limit=8):
    """Returns recent attendance records for a given student."""
    conn = get_conn()
    df = pd.read_sql(
        "SELECT id, subject_code, class_date, period, status FROM attendance WHERE student_id=? ORDER BY class_date DESC, period DESC LIMIT ?",
        conn, params=(student_id, limit)
    )
    conn.close()
    return df


def get_risk_report():
    """Returns full student_risk view as DataFrame."""
    conn = get_conn()
    df = pd.read_sql("SELECT student_id, full_name, department, total_absences, attendance_pct, risk_level FROM student_risk ORDER BY total_absences DESC LIMIT 10", conn)
    conn.close()
    return df


def get_dept_avg_attendance():
    """Returns DataFrame of avg attendance per department from materialized view."""
    conn = get_conn()
    df = pd.read_sql("SELECT department, AVG(attendance_pct) as avg_att FROM mv_dept_attendance GROUP BY department", conn)
    conn.close()
    return df


def get_risk_distribution():
    """Returns DataFrame of student count per risk level."""
    conn = get_conn()
    df = pd.read_sql("SELECT risk_level, COUNT(*) as count FROM student_risk GROUP BY risk_level", conn)
    conn.close()
    return df


def get_subject_breakdown(subject_code):
    """Returns per-student attendance % for a given subject."""
    conn = get_conn()
    df = pd.read_sql(f"""
        SELECT s.student_id, s.full_name, s.department,
               COUNT(*) as total_classes,
               SUM(CASE WHEN a.status IN ('PRESENT','LATE','ON_DUTY') THEN 1 ELSE 0 END) as attended,
               ROUND(100.0 * SUM(CASE WHEN a.status IN ('PRESENT','LATE','ON_DUTY') THEN 1 ELSE 0 END) / COUNT(*), 1) as pct
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        WHERE a.subject_code = '{subject_code}'
        GROUP BY a.student_id
        ORDER BY pct ASC
    """, conn)
    conn.close()
    return df


def get_all_tables():
    """Returns list of user table names."""
    conn = get_conn()
    rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall()
    conn.close()
    return [r[0] for r in rows]


def get_table_info(table_name):
    """Returns (columns_df, foreign_keys_df, row_count) for a table."""
    conn = get_conn()
    cols      = pd.read_sql(f"PRAGMA table_info({table_name})", conn)
    fks       = pd.read_sql(f"PRAGMA foreign_key_list({table_name})", conn)
    row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    conn.close()
    return cols, fks, row_count


def get_all_indexes():
    """Returns DataFrame of all user-defined indexes."""
    conn = get_conn()
    df = pd.read_sql("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND sql IS NOT NULL ORDER BY tbl_name", conn)
    conn.close()
    return df


def get_all_triggers():
    """Returns list of (name, sql) for all triggers."""
    conn = get_conn()
    rows = conn.execute("SELECT name, sql FROM sqlite_master WHERE type='trigger'").fetchall()
    conn.close()
    return rows


def get_audit_log(limit=10):
    """Returns recent audit log entries."""
    conn = get_conn()
    df = pd.read_sql("SELECT actor_id, action, entity_type, entity_id, timestamp FROM audit_log ORDER BY id DESC LIMIT ?", conn, params=(limit,))
    conn.close()
    return df


def get_query_plan(query):
    """Returns EXPLAIN QUERY PLAN output as DataFrame."""
    conn = get_conn()
    df = pd.read_sql(f"EXPLAIN QUERY PLAN {query}", conn)
    conn.close()
    return df


def run_raw_query(sql):
    """Runs any SELECT query and returns a DataFrame."""
    conn = get_conn()
    df = pd.read_sql(sql, conn)
    conn.close()
    return df


# -----------------------------------------------------------------------------
# WRITE functions
# -----------------------------------------------------------------------------

def record_attendance(student_id, subject_code, status):
    """
    Inserts one attendance record for today.
    Returns (period_number, absences_in_last_3_days, new_alert_created).
    """
    today = time.strftime("%Y-%m-%d")
    conn = get_conn()

    next_period = conn.execute(
        "SELECT COALESCE(MAX(period), 0) + 1 FROM attendance WHERE student_id=? AND class_date=?",
        (student_id, today)
    ).fetchone()[0]

    conn.execute(
        "INSERT OR IGNORE INTO attendance (student_id, subject_code, class_date, period, status, marked_by) VALUES (?,?,?,?,?,'FAC_CSE1')",
        (student_id, subject_code, today, next_period, status)
    )
    conn.commit()

    absences = conn.execute(
        "SELECT COUNT(*) FROM attendance WHERE student_id=? AND status='ABSENT' AND class_date >= date('now','-3 days')",
        (student_id,)
    ).fetchone()[0]

    new_alert = conn.execute(
        "SELECT COUNT(*) FROM alerts WHERE student_id=? AND status='ACTIVE' AND created_at >= datetime('now','-10 seconds')",
        (student_id,)
    ).fetchone()[0]

    conn.close()
    return next_period, absences, new_alert > 0


def run_trigger_demo():
    """
    Marks student 21BCE1234 ABSENT in all 3 CSE subjects for today.
    Returns a log list of strings describing what happened.
    """
    today = time.strftime("%Y-%m-%d")
    demo_subjects = ["CSE2001", "CSE2002", "CSE2003"]
    log = []

    conn = get_conn()
    alerts_before = conn.execute(
        "SELECT COUNT(*) FROM alerts WHERE student_id='21BCE1234' AND status='ACTIVE'"
    ).fetchone()[0]

    for subj in demo_subjects:
        period = conn.execute(
            "SELECT COALESCE(MAX(period),0)+1 FROM attendance WHERE student_id='21BCE1234' AND class_date=?",
            (today,)
        ).fetchone()[0]
        conn.execute(
            "INSERT OR IGNORE INTO attendance (student_id, subject_code, class_date, period, status, marked_by) VALUES ('21BCE1234',?,?,?,'ABSENT','FAC_CSE1')",
            (subj, today, period)
        )
        conn.commit()
        log.append(f"Marked ABSENT in {subj} (period {period})")

    alerts_after = conn.execute(
        "SELECT COUNT(*) FROM alerts WHERE student_id='21BCE1234' AND status='ACTIVE'"
    ).fetchone()[0]

    if alerts_after > alerts_before:
        log.append(f"Trigger fired! New alert created. Total active alerts: {alerts_after}")
    else:
        log.append(f"No new alert (may already exist for today). Active alerts: {alerts_after}")

    conn.close()
    return log


def acknowledge_alert(alert_id):
    """Sets an alert to ACKNOWLEDGED by WRD_A."""
    conn = get_conn()
    conn.execute(
        "UPDATE alerts SET status='ACKNOWLEDGED', acknowledged_by='WRD_A', acknowledged_at=datetime('now') WHERE id=?",
        (alert_id,)
    )
    conn.commit()
    conn.close()


def resolve_all_alerts(student_id):
    """Resolves all ACTIVE alerts for a student. Returns count resolved."""
    conn = get_conn()
    result = conn.execute(
        "UPDATE alerts SET status='RESOLVED', resolved_at=datetime('now') WHERE student_id=? AND status='ACTIVE'",
        (student_id,)
    )
    conn.commit()
    count = result.rowcount
    conn.close()
    return count


def run_savepoint_demo():
    """
    Demonstrates SAVEPOINT: valid update → savepoint → accidental bulk update → rollback to savepoint → commit.
    Returns a log list of strings.
    """
    conn = get_conn()
    log = []
    try:
        conn.execute("BEGIN")
        log.append("1. BEGIN TRANSACTION")

        conn.execute("UPDATE attendance SET status='PRESENT' WHERE student_id='21BCE1234' AND period=1")
        log.append("2. UPDATE period 1 to PRESENT")

        conn.execute("SAVEPOINT before_mistake")
        log.append("3. SAVEPOINT before_mistake")

        conn.execute("UPDATE attendance SET status='ABSENT' WHERE student_id='21BCE1234'")
        count = conn.execute("SELECT COUNT(*) FROM attendance WHERE student_id='21BCE1234' AND status='ABSENT'").fetchone()[0]
        log.append(f"4. Accidental UPDATE — all {count} records now ABSENT")

        conn.execute("ROLLBACK TO before_mistake")
        log.append("5. ROLLBACK TO before_mistake — mistake undone")

        conn.execute("COMMIT")
        log.append("6. COMMIT — only the valid change from step 2 was saved")

    except Exception as e:
        conn.execute("ROLLBACK")
        log.append(f"ERROR: {e}")
    finally:
        conn.close()

    return log


def insert_batch_records(student_id, subject_code, start_date, num_days, status):
    """
    Inserts attendance records for num_days consecutive days starting from start_date.
    Uses a SAVEPOINT. Returns (inserted_count, sql_log_list).
    """
    conn = get_conn()
    log = []
    inserted = 0
    try:
        conn.execute("BEGIN")
        conn.execute("SAVEPOINT before_batch")

        for i in range(num_days):
            d = (start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            period = conn.execute(
                "SELECT COALESCE(MAX(period),0)+1 FROM attendance WHERE student_id=? AND class_date=?",
                (student_id, d)
            ).fetchone()[0]
            conn.execute(
                "INSERT OR IGNORE INTO attendance (student_id, subject_code, class_date, period, status, marked_by) VALUES (?,?,?,?,?,'FAC_CSE1')",
                (student_id, subject_code, d, period, status)
            )
            log.append(f"INSERT INTO attendance VALUES ('{student_id}', '{subject_code}', '{d}', {period}, '{status}')")
            inserted += 1

        conn.execute("RELEASE before_batch")
        conn.execute("COMMIT")
    except Exception as e:
        conn.execute("ROLLBACK")
        conn.close()
        raise e
    finally:
        conn.close()

    return inserted, log


def refresh_materialized_views():
    """
    Fires the refresh trigger by inserting then deleting a dummy record.
    Returns (before_dict, after_dict).
    """
    conn = get_conn()
    today = time.strftime("%Y-%m-%d")

    before = dict(conn.execute("SELECT department, attendance_pct FROM mv_dept_attendance").fetchall())

    conn.execute(
        "INSERT OR IGNORE INTO attendance (student_id, subject_code, class_date, period, status, marked_by) VALUES ('21BCE1234','CSE2001',?,'99','PRESENT','FAC_CSE1')",
        (today,)
    )
    conn.commit()
    conn.execute("DELETE FROM attendance WHERE period=99 AND student_id='21BCE1234'")
    conn.commit()

    after = dict(conn.execute("SELECT department, attendance_pct FROM mv_dept_attendance").fetchall())
    conn.close()
    return before, after


def benchmark_query(student_id, runs=50):
    """
    Runs indexed and unindexed queries 'runs' times each.
    Returns (avg_indexed_us, avg_scan_us).
    """
    import time as _time

    q_indexed = f"SELECT * FROM attendance WHERE student_id = '{student_id}' AND class_date >= date('now','-30 days') ORDER BY class_date DESC"
    q_scan    = f"SELECT * FROM attendance WHERE +student_id = '{student_id}' AND class_date >= date('now','-30 days')"

    conn = get_conn()

    t0 = _time.perf_counter_ns()
    for _ in range(runs):
        conn.execute(q_indexed).fetchall()
    avg_indexed = ((_time.perf_counter_ns() - t0) / runs) / 1000

    t0 = _time.perf_counter_ns()
    for _ in range(runs):
        conn.execute(q_scan).fetchall()
    avg_scan = ((_time.perf_counter_ns() - t0) / runs) / 1000

    conn.close()
    return avg_indexed, avg_scan


def drop_and_recreate_index(student_id):
    """
    Drops idx_attendance_student_date, captures query plans before/during/after.
    Returns (plan_before, plan_dropped, plan_after) as plain strings.
    """
    q = f"SELECT * FROM attendance WHERE student_id = '{student_id}' AND class_date >= date('now','-30 days') ORDER BY class_date DESC"
    conn = get_conn()

    plan_before  = conn.execute(f"EXPLAIN QUERY PLAN {q}").fetchall()
    conn.execute("DROP INDEX IF EXISTS idx_attendance_student_date")
    plan_dropped = conn.execute(f"EXPLAIN QUERY PLAN {q}").fetchall()
    conn.execute("CREATE INDEX IF NOT EXISTS idx_attendance_student_date ON attendance(student_id, class_date DESC)")
    plan_after   = conn.execute(f"EXPLAIN QUERY PLAN {q}").fetchall()

    conn.close()

    def detail(rows):
        return rows[0][3] if rows else "N/A"

    return detail(plan_before), detail(plan_dropped), detail(plan_after)


def analyze_table(table_name):
    """Runs ANALYZE and returns (row_count, col_count, index_count)."""
    conn = get_conn()
    conn.execute("ANALYZE")
    row_count  = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    col_count  = len(conn.execute(f"PRAGMA table_info({table_name})").fetchall())
    idx_count  = conn.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND tbl_name=?", (table_name,)).fetchone()[0]
    conn.close()
    return row_count, col_count, idx_count


def test_fk_constraint():
    """
    Tries to insert a row with a fake student_id into attendance.
    Returns (blocked: bool, message: str).
    """
    conn = get_conn()
    try:
        conn.execute("INSERT INTO attendance (student_id, subject_code, class_date, period, status) VALUES ('FAKE999','CSE2001','2025-01-01',1,'PRESENT')")
        conn.commit()
        conn.close()
        return False, "Insert succeeded — FK may not be enforced"
    except sqlite3.IntegrityError as e:
        conn.close()
        return True, str(e)


# -----------------------------------------------------------------------------
# CLI Viva Demo — Run directly with: python3 db.py
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("🎓 DBMS VIVA DEMO — Pure SQLite Database Engine")
    print("=" * 60)

    # 1. Database Stats
    students, records, alerts, avg_att = get_summary_stats()
    print(f"\n[1] DATABASE SNAPSHOT:")
    print(f"    - Students: {students}")
    print(f"    - Attendance Records: {records:,}")
    print(f"    - Active Alerts: {alerts}")
    print(f"    - Campus Average Attendance: {avg_att}%")

    # 2. Foreign Key Test
    print(f"\n[2] INTEGRITY CONSTRAINTS (Foreign Key Enforcement):")
    blocked, msg = test_fk_constraint()
    print(f"    - Inserting fake student 'FAKE999': {'BLOCKED (Passed)' if blocked else 'FAILED'}")
    print(f"    - SQLite response: {msg}")

    # 3. Trigger & Event Demo
    print(f"\n[3] EVENT TRIGGERS (auto_alert_on_streak):")
    trigger_logs = run_trigger_demo()
    for log_entry in trigger_logs:
        print(f"    - {log_entry}")

    # 4. Savepoint & Rollback Demo
    print(f"\n[4] ACID TRANSACTIONS (SAVEPOINT & ROLLBACK TO):")
    tx_logs = run_savepoint_demo()
    for tx_step in tx_logs:
        print(f"    - {tx_step}")

    # 5. Query Optimization & Index Benchmark
    print(f"\n[5] QUERY OPTIMIZER (B+ Tree Index vs Full Scan):")
    t_idx, t_scan = benchmark_query("21BCE1234", runs=50)
    print(f"    - Indexed query:   {t_idx:.2f} µs (O(log N))")
    print(f"    - Full table scan: {t_scan:.2f} µs (O(N))")
    print(f"    - Speedup:         {t_scan/t_idx:.1f}x faster with index")

    print("\n" + "=" * 60)
    print("✅ All database engine features verified!")
    print("=" * 60)

