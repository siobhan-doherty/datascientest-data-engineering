from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.engine import create_engine
import os


server = FastAPI(title = "User API")

# read DB creds from env
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DBNAME = os.getenv("MYSQL_DATABASE", "Main")

# build SQLAlchemy URL
conn_url = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DBNAME}"
engine = create_engine(conn_url)

class User(BaseModel):
    user_id: int
    username: str
    email: str

@server.get("/status")
async def status():
    return {"status": 1}

@server.get("/users", response_model = list[User])
async def list_users():
    with engine.connect() as conn:
        rows = conn.execute("SELECT id, username, email FROM Users;").fetchall()

    return [User(user_id = r[0], username = r[1], email = r[2]) for r in rows]

@server.get("/users/{user_id}", response_model = User)
async def get_user(user_id: int):
    with engine.connect() as conn:
        rows = conn.execute(
            "SELECT id, username, email FROM Users WHERE id = %s;", (user_id,)
        ).fetchall()
    if not rows:
        raise HTTPException(404, "Unknown User ID")
    r = rows[0]

    return User(user_id = r[0], username = r[1], email = r[2])
