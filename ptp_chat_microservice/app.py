from fastapi import FastAPI
from router import router as ptp_chat_router
from utils.add_data import router as fixtures_router

app = FastAPI(
    title='PtpСhat'
)

app.include_router(ptp_chat_router)
app.include_router(fixtures_router)
