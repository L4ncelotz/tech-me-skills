import sqlite3
from fastapi import FastAPI

app = FastAPI(title="Equipment Tracker")


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect("equipment.db")
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
