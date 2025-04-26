from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient

import food
from auth import FatSecretAuth

auth = FatSecretAuth(
    token_url="https://oauth.fatsecret.com/connect/token",
    client_id="",
    client_secret=""
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncClient(auth=auth) as client:
        yield {
            "client": client
        }

app = FastAPI(lifespan=lifespan)
app.include_router(food.router)

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
