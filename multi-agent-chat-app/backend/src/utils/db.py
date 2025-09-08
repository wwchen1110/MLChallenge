import sqlite3
from typing import Any, List, Dict

DB_PATH = "patients.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            name TEXT,
            dob TEXT,
            pcp TEXT,
            ehr_id TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS referred_providers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            provider_name TEXT,
            specialty TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            date TEXT,
            time TEXT,
            provider_name TEXT,
            status TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
        )
    """)
    conn.commit()
    conn.close()

def insert_patient(patient: Dict[str, Any]):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO patients (patient_id, name, dob, pcp, ehr_id) VALUES (?, ?, ?, ?, ?)",
              (patient["id"], patient["name"], patient["dob"], patient["pcp"], patient["ehrId"]))
    conn.commit()
    conn.close()

def insert_referred_providers(patient_id: str, providers: List[Dict[str, Any]]):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for provider in providers:
        c.execute("INSERT INTO referred_providers (patient_id, provider_name, specialty) VALUES (?, ?, ?)",
                  (patient_id, provider.get("provider"), provider.get("specialty")))
    conn.commit()
    conn.close()

def insert_appointments(patient_id: str, appointments: List[Dict[str, Any]]):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for appt in appointments:
        c.execute("INSERT INTO appointments (patient_id, date, time, provider_name, status) VALUES (?, ?, ?, ?, ?)",
                  (patient_id, appt.get("date"), appt.get("time"), appt.get("provider"), appt.get("status")))
    conn.commit()
    conn.close()

def get_patient(patient_id: str) -> Dict[str, Any]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT patient_id, name, dob, pcp, ehr_id FROM patients WHERE patient_id = ?", (patient_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return {}
    patient = {
        "patient_id": row[0],
        "name": row[1],
        "dob": row[2],
        "pcp": row[3],
        "ehr_id": row[4]
    }
    c.execute("SELECT provider_name, specialty FROM referred_providers WHERE patient_id = ?", (patient_id,))
    patient["referred_providers"] = [{"provider_name": r[0], "specialty": r[1]} for r in c.fetchall()]
    c.execute("SELECT date, time, provider_name, status FROM appointments WHERE patient_id = ?", (patient_id,))
    patient["appointments"] = [{"date": r[0], "time": r[1], "provider_name": r[2], "status": r[3]} for r in c.fetchall()]
    conn.close()
    return patient