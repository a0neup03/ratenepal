
from fastapi import Header, HTTPException, Depends
import os

API_KEY = os.getenv("API_KEY", "default_api_key")

async def get_api_key(api_key: str = Header(None)):
    if not api_key or api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key
