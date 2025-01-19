from fastapi import FastAPI

app = FastAPI(
    title="QuantAI Finance Chatbot",
    version="0.1.0",
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def root():
    return {"message": "Welcome to the QuantAI Finance Chatbot!"}
