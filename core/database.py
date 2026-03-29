import sqlite3
import os
from config import log

DB_PATH = os.path.join(os.path.dirname(__file__), "../protoqol_mvp.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Clients Table (B2B API Keys)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            api_key TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. Deeds History Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deeds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            nomad_id TEXT,
            mission_id TEXT,
            verdict TEXT,
            impact_points INTEGER,
            tx_hash TEXT,
            integrity_hash TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(client_id) REFERENCES clients(id)
        )
    ''')
    
    # Add a default test client for the pitch
    cursor.execute("INSERT OR IGNORE INTO clients (name, api_key) VALUES ('Aqtobe_B2B_Partner', 'PQ_LIVE_DEMO_SECRET')")
    
    conn.commit()
    conn.close()
    log.info("[DB_GATEWAY] SQLite MVP Database Initialized ✓")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
