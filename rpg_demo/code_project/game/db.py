# game/db.py

import sqlite3
import os

DB_FILENAME = "npc_memory.db"

def init_db(db_filename=DB_FILENAME):
    project_root = os.path.dirname(os.path.dirname(__file__))
    db_path = os.path.join(project_root, db_filename)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player TEXT NOT NULL,
            npc TEXT NOT NULL,
            memory TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

def save_npc_memory(npc_name: str, player_name: str, memory: str, db_filename=DB_FILENAME):
    project_root = os.path.dirname(os.path.dirname(__file__))
    db_path = os.path.join(project_root, db_filename)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        "INSERT INTO memories (player, npc, memory) VALUES (?, ?, ?);",
        (player_name, npc_name, memory)
    )
    conn.commit()
    conn.close()

def load_npc_memory(npc_name: str, player_name: str, limit: int = 1000, db_filename=DB_FILENAME):
    project_root = os.path.dirname(os.path.dirname(__file__))
    db_path = os.path.join(project_root, db_filename)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        "SELECT memory FROM memories WHERE npc = ? AND player = ? ORDER BY id;",
        (npc_name, player_name)
    )
    rows = c.fetchall()
    conn.close()
    # devuelve toda la historia cronológica
    return [row[0] for row in rows]
