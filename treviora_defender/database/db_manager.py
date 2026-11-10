r"""
TREVIORA AI DEFENDER - SQLite Database Manager
All database records persist strictly at D:\projects\antivirus\data\defender.db
"""
import sqlite3
import threading
from datetime import datetime
from pathlib import Path
from treviora_defender.config.constants import DB_PATH, DATA_DIR
from treviora_defender.utils.logger import get_logger

logger = get_logger()


class DatabaseManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DatabaseManager, cls).__new__(cls)
                cls._instance._init_db()
            return cls._instance

    def _init_db(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.db_path = str(DB_PATH)
        self._local = threading.local()

        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Threats table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS threats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT NOT NULL,
                    file_hash TEXT,
                    threat_name TEXT NOT NULL,
                    category TEXT,
                    severity TEXT,
                    risk_score INTEGER,
                    detection_method TEXT,
                    ai_explanation TEXT,
                    status TEXT DEFAULT 'Active',
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Scans history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scan_type TEXT NOT NULL,
                    target_path TEXT,
                    start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    end_time DATETIME,
                    files_scanned INTEGER DEFAULT 0,
                    threats_found INTEGER DEFAULT 0,
                    duration_seconds REAL DEFAULT 0,
                    status TEXT DEFAULT 'Completed'
                )
            """)

            # Quarantine table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quarantine (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_path TEXT NOT NULL,
                    quarantine_filename TEXT NOT NULL,
                    file_hash TEXT NOT NULL,
                    file_size INTEGER DEFAULT 0,
                    threat_name TEXT,
                    quarantined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_restored INTEGER DEFAULT 0
                )
            """)

            # Security Events table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS security_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    source TEXT,
                    description TEXT,
                    severity TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Known Malware Hashes cache table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS known_hashes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sha256 TEXT UNIQUE NOT NULL,
                    threat_name TEXT NOT NULL,
                    category TEXT,
                    severity TEXT
                )
            """)

            # Index for fast hash lookup
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_known_hashes_sha256 ON known_hashes(sha256)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_threats_status ON threats(status)")

            conn.commit()
            logger.info(f"Database initialized successfully at {self.db_path}")

    def get_connection(self):
        return sqlite3.connect(self.db_path, timeout=15)

    # Threat operations
    def add_threat(self, file_path, file_hash, threat_name, category, severity,
                   risk_score, detection_method, ai_explanation, status="Active"):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO threats (file_path, file_hash, threat_name, category, severity,
                                    risk_score, detection_method, ai_explanation, status, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (file_path, file_hash, threat_name, category, severity, risk_score,
                  detection_method, ai_explanation, status, datetime.now().isoformat()))
            conn.commit()
            return cursor.lastrowid

    def get_active_threats(self):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM threats WHERE status = 'Active' ORDER BY id DESC")
            return [dict(row) for row in cursor.fetchall()]

    def get_all_threats(self, limit=100):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM threats ORDER BY id DESC LIMIT ?", (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def update_threat_status(self, threat_id, status):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE threats SET status = ? WHERE id = ?", (status, threat_id))
            conn.commit()

    # Scan operations
    def log_scan_start(self, scan_type, target_path=""):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO scans (scan_type, target_path, start_time, status)
                VALUES (?, ?, ?, 'Running')
            """, (scan_type, target_path, datetime.now().isoformat()))
            conn.commit()
            return cursor.lastrowid

    def log_scan_end(self, scan_id, files_scanned, threats_found, duration_seconds, status="Completed"):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE scans 
                SET end_time = ?, files_scanned = ?, threats_found = ?, duration_seconds = ?, status = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), files_scanned, threats_found, duration_seconds, status, scan_id))
            conn.commit()

    def get_scan_history(self, limit=50):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM scans ORDER BY id DESC LIMIT ?", (limit,))
            return [dict(row) for row in cursor.fetchall()]

    # Quarantine operations
    def add_quarantine(self, original_path, quarantine_filename, file_hash, file_size, threat_name):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO quarantine (original_path, quarantine_filename, file_hash, file_size, threat_name, quarantined_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (original_path, quarantine_filename, file_hash, file_size, threat_name, datetime.now().isoformat()))
            conn.commit()
            return cursor.lastrowid

    def get_quarantined_files(self):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM quarantine WHERE is_restored = 0 ORDER BY id DESC")
            return [dict(row) for row in cursor.fetchall()]

    def mark_quarantine_restored(self, quarantine_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE quarantine SET is_restored = 1 WHERE id = ?", (quarantine_id,))
            conn.commit()

    def delete_quarantine_record(self, quarantine_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM quarantine WHERE id = ?", (quarantine_id,))
            conn.commit()

    # Security Events
    def log_event(self, event_type, source, description, severity="Info"):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO security_events (event_type, source, description, severity, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (event_type, source, description, severity, datetime.now().isoformat()))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed logging event: {e}")

    def get_recent_events(self, limit=50):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM security_events ORDER BY id DESC LIMIT ?", (limit,))
            return [dict(row) for row in cursor.fetchall()]

    # Stats for Dashboard
    def get_dashboard_stats(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM threats WHERE status = 'Active'")
            active_threats = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM threats")
            total_threats = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM quarantine WHERE is_restored = 0")
            quarantined_count = cursor.fetchone()[0]

            cursor.execute("SELECT SUM(files_scanned) FROM scans")
            scanned_res = cursor.fetchone()[0]
            total_scanned = scanned_res if scanned_res is not None else 0

            cursor.execute("SELECT COUNT(*) FROM scans")
            total_scans = cursor.fetchone()[0]

            return {
                "active_threats": active_threats,
                "total_threats": total_threats,
                "quarantined_count": quarantined_count,
                "total_scanned": total_scanned,
                "total_scans": total_scans
            }

    # Hash database matching
    def check_known_hash(self, sha256_hash: str):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM known_hashes WHERE sha256 = ?", (sha256_hash.lower(),))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def populate_seed_threat_hashes(self, seed_list):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            for item in seed_list:
                cursor.execute("""
                    INSERT OR IGNORE INTO known_hashes (sha256, threat_name, category, severity)
                    VALUES (?, ?, ?, ?)
                """, (item["sha256"].lower(), item["name"], item["category"], item["severity"]))
            conn.commit()
