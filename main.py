from fastapi import FastAPI, Query
from sqlalchemy import create_engine, text
import os

app = FastAPI()

# PostgreSQL Database Connection
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

            # Handle different result formats
            if result.returns_rows:
                rows = result.fetchall()

                # If the query returns a single row with a single value (like COUNT)
                if len(rows) == 1 and len(rows[0]) == 1:
                    return {"result": rows[0][0]}
                
                # Convert row results to dictionaries
                return {"data": [dict(row._mapping) for row in rows]}
            else:
                return {"message": "Query executed successfully, but no rows returned."}

    except Exception as e:
        return {"error": str(e)}
