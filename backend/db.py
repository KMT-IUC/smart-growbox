import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("kabin.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS olcumler (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            zaman     TEXT NOT NULL,
            sicaklik  REAL,
            nem       REAL,
            co2       INTEGER,
            toprak_nemi REAL,
            pompa_aktif INTEGER,
            fan_aktif   INTEGER
        )
    """)
    conn.commit()
    return conn

def kaydet(conn, veri: dict):
    conn.execute("""
        INSERT INTO olcumler
        (zaman, sicaklik, nem, co2, toprak_nemi, pompa_aktif, fan_aktif)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        veri.get("sicaklik"),
        veri.get("nem"),
        veri.get("co2"),
        veri.get("toprak_nemi"),
        veri.get("pompa_aktif"),
        veri.get("fan_aktif"),
    ))
    conn.commit()

def son_olcum(conn) -> dict:
    row = conn.execute(
        "SELECT * FROM olcumler ORDER BY id DESC LIMIT 1"
    ).fetchone()
    return dict(row) if row else {}

def gecmis(conn, limit: int) -> list:
    rows = conn.execute(
        "SELECT * FROM olcumler ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    return [dict(r) for r in rows]