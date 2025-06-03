from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import httpx
import base64

app = FastAPI()

# CORS (если нужно проверять из браузера)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Простые учетные данные
USERNAME = "user"
PASSWORD = "pass"

@app.middleware("http")
async def auth_proxy(request: Request, call_next):
    auth_header = request.headers.get("authorization")
    expected = "Basic " + base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()

    if auth_header != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Получаем URL из параметра запроса
    target_url = request.query_params.get("url")
    if not target_url:
        raise HTTPException(status_code=400, detail="Missing 'url' parameter")

    # Проксируем запрос
    try:
        async with httpx.AsyncClient() as client:
            proxy_response = await client.get(target_url)
        return Response(
            content=proxy_response.content,
            status_code=proxy_response.status_code,
            headers=proxy_response.headers,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
