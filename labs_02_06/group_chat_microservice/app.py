from fastapi import FastAPI
from router import router as chat_router
from utils.add_data import router as fixtures_router

app = FastAPI(
    title='GroupChat',
)

app.include_router(chat_router)
app.include_router(fixtures_router)
