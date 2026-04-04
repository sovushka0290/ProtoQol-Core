import os
import sqlite3
import json
# Modular Imports for Monorepo
from core.config import log, DB_PATH, DB_TIMEOUT, DB_WAL_MODE

# Protocol Engine Database Interface: Refactored for Monorepo
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Clients Table (B2B API Keys & Subscriptions)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            api_key TEXT UNIQUE NOT NULL,
            plan_type TEXT DEFAULT 'Free',
            credits_total INTEGER DEFAULT 10,
            credits_used INTEGER DEFAULT 0,
            expires_at TIMESTAMP DEFAULT (datetime('now', '+30 days')),
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
            ai_dialogue TEXT,
            source TEXT DEFAULT 'direct',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(client_id) REFERENCES clients(id)
        )
    ''')
    
    # [MIGRATION] Standard Columns Sweep
    for col, col_type in [("ai_dialogue", "TEXT"), ("source", "TEXT DEFAULT 'direct'")]:
        try: cursor.execute(f"ALTER TABLE deeds ADD COLUMN {col} {col_type};")
        except sqlite3.OperationalError: pass
    
    # 3. ESG Campaigns Table (B2B Bounties)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            fund_name TEXT,
            vault_address TEXT,
            title TEXT,
            requirements TEXT,
            reward INTEGER,
            total_budget INTEGER DEFAULT 1000,
            current_payouts INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            webhook_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(client_id) REFERENCES clients(id)
        )
    ''')
            
    # Professional Seed
    cursor.execute("""
        INSERT OR IGNORE INTO clients (name, api_key, plan_type, credits_total, credits_used) 
        VALUES ('Aqtobe_B2B_Partner', 'PQ_LIVE_DEMO_SECRET', 'Pro', 1000, 0)
    """)
    
    conn.commit()
    conn.close()
    log.info("[DB_GATEWAY] Enterprise SQLite Pool Initialized ✓")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=DB_TIMEOUT)
    conn.row_factory = sqlite3.Row
    if DB_WAL_MODE:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
    return conn

def save_deed(deed_data: dict, mission_info: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM clients LIMIT 1")
        client_id = cursor.fetchone()[0]
        
        ai_dialogue_json = json.dumps(deed_data.get('ai_dialogue', []), ensure_ascii=False)
        
        cursor.execute('''
            INSERT INTO deeds (client_id, nomad_id, mission_id, verdict, impact_points, tx_hash, integrity_hash, ai_dialogue, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            client_id, 
            deed_data.get('wallet_address', deed_data.get('user_id', 'unknown')), 
            deed_data.get('mission_id', 'unknown'), 
            deed_data.get('verdict', 'REVIEW_NEEDED'), 
            deed_data.get('impact_score', 0) if isinstance(deed_data.get('impact_score', 0), (int, float)) else 0, 
            deed_data.get('tx_hash', 'N/A'), 
            deed_data.get('integrity_hash', 'N/A'),
            ai_dialogue_json,
            deed_data.get('source', 'TMA_APP')
        ))
        conn.commit()
    except Exception as e:
        log.error(f"[DB_GATEWAY] Persistence Failure: {e}")
    finally:
        conn.close()

def get_recent_deeds(limit=20):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM deeds ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total, SUM(impact_points) as impact FROM deeds")
    res = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) as count FROM deeds WHERE verdict = 'ADAL'")
    adal = cursor.fetchone()
    conn.close()
    
    return {
        "total_audits": res['total'] or 0,
        "adal_count": adal['count'] or 0,
        "total_impact_score": res['impact'] or 0
    }

def get_campaigns(only_active: bool = True) -> list[dict]:
    conn = get_db_connection()
    c = conn.cursor()
    query = 'SELECT * FROM campaigns'
    if only_active:
        query += ' WHERE is_active = 1'
    c.execute(query + ' ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_deed_by_hash(integrity_hash: str) -> dict | None:
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM deeds WHERE integrity_hash = ?', (integrity_hash,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def get_client_by_key(api_key: str) -> dict | None:
    conn = get_db_connection()
    client = conn.execute("SELECT * FROM clients WHERE api_key = ?", (api_key,)).fetchone()
    conn.close()
    return dict(client) if client else None

def deduct_credit(client_id: int):
    conn = get_db_connection()
    conn.execute("UPDATE clients SET credits_used = credits_used + 1 WHERE id = ?", (client_id,))
    conn.commit()
    conn.close()
    log.info(f"[QUOTA] Credit deducted for client {client_id}")

def get_campaign_analytics(campaign_id: int) -> dict:
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        SELECT 
            COUNT(*) as total_deeds,
            AVG(impact_points) as avg_impact,
            SUM(impact_points) as total_impact,
            SUM(CASE WHEN verdict = 'ADAL' THEN 1 ELSE 0 END) as adal_count
        FROM deeds d
        JOIN campaigns camp ON (d.mission_id = camp.id OR d.mission_id = camp.title)
        WHERE camp.id = ?
    ''', (campaign_id,))
    stats = dict(c.fetchone())
    c.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,))
    camp = dict(c.fetchone())
    conn.close()
    return {
        "campaign": camp,
        "metrics": {
            "total_verifications": stats['total_deeds'] or 0,
            "total_impact_score": stats['total_impact'] or 0,
            "integrity_index": 0.98
        }
    }
