from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from db.database import create_all_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all_tables()

    yield


app = FastAPI(
    title="AI-Summarizer-API",
    description="API for summarizing content",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_headers=["*"], allow_methods=["*"]
)


@app.get("/healthcheck")
def healthcheck():
    return {"ok": True, "msg": "API online"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=settings.DEBUG)
