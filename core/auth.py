from fastapi import Header, HTTPException, Depends
from core.database import get_db_connection

async def get_api_key(x_api_key: str = Header(...)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="X-API-Key header is missing.")
    
    conn = get_db_connection()
    client = conn.execute("SELECT * FROM clients WHERE api_key = ?", (x_api_key,)).fetchone()
    conn.close()
    
    if not client:
        raise HTTPException(status_code=403, detail="Invalid API Key. Unauthorized access.")
    
    return client
