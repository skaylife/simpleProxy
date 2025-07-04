from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# Настройка CORS (если нужно)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/proxy")
async def proxy(url: str):
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
            return {
                "status": r.status_code,
                "headers": dict(r.headers),
                "text": r.text
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
