from fastapi import FastAPI, Query
from sqlalchemy import create_engine, text
import os

app = FastAPI()

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@your-db-host:5432/dbname")
engine = create_engine(DATABASE_URL)

@app.get("/")
def read_root():
    return {"message": "GPT-PostgreSQL API is running!"}

@app.get("/query")
async def run_query(query: str = Query(..., description="SQL query to execute")):
    """
    Executes a given SQL query and returns the results.
    Example: /query?query=SELECT%20*%20FROM%20users
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            return {"data": [dict(row) for row in result]}
    except Exception as e:
        return {"error": str(e)}
