from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import httpx
import base64

app = FastAPI()

# Настройка CORS (если нужно)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USERNAME = "proxyuser"
PASSWORD = "proxypass"

# Middleware для проверки Basic Auth
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth = request.headers.get("authorization")
        if not auth or not auth.startswith("Basic "):
            raise HTTPException(status_code=401, detail="Unauthorized")

        try:
            credentials = base64.b64decode(auth.split(" ")[1]).decode("utf-8")
            username, password = credentials.split(":")
        except:
            raise HTTPException(status_code=401, detail="Unauthorized")

        if username != USERNAME or password != PASSWORD:
            raise HTTPException(status_code=401, detail="Unauthorized")

        return await call_next(request)

app.add_middleware(AuthMiddleware)

@app.get("/proxy")
async def proxy(url: str):
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
            return {"status": r.status_code, "headers": dict(r.headers), "text": r.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
