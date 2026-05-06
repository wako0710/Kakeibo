from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 全てのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "家計簿アプリAPIへようこそ！"}


# --- データベース接続 & テーブル作成 ---
def init_db():
    conn = sqlite3.connect("kakeibo.db")
    cur = conn.cursor()

    # 収支テーブル作成
    cur.execute("""
        CREATE TABLE IF NOT EXISTS kakeibo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount INTEGER,
            memo TEXT
        )
    """)

    conn.commit()
    conn.close()

# サーバー起動時に DB を初期化
init_db()
from pydantic import BaseModel
import sqlite3


# --- データモデル（受け取るデータの形） ---
class KakeiboItem(BaseModel):
    date: str
    category: str
    amount: int
    memo: str

# --- データ登録API ---
@app.post("/add")
def add_item(item: KakeiboItem):
    conn = sqlite3.connect("kakeibo.db")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO kakeibo (date, category, amount, memo)
        VALUES (?, ?, ?, ?)
    """, (item.date, item.category, item.amount, item.memo))

    conn.commit()
    conn.close()

    return {"status": "success", "data": item}

@app.get("/list")
def get_list():
    conn = sqlite3.connect("kakeibo.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM kakeibo")
    rows = cur.fetchall()

    conn.close()

    # データを辞書形式に変換
    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "date": r[1],
            "category": r[2],
            "amount": r[3],
            "memo": r[4]
        })

    return {"data": result}

import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
