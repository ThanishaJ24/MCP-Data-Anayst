from fastapi import FastAPI, UploadFile, File,Form
import shutil
import os

from app.upload import process_file
from app.ai_agent import ask_agent

app = FastAPI()

UPLOAD_FOLDER = "app/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {"message": "MCP Data Analyst API"}

# Upload endpoint
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_FOLDER}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    table_name = file.filename.split(".")[0]

    result = process_file(file_path, table_name)

    return result

# Ask AI endpoint
@app.post("/ask")
async def ask(question: str = Form(...)):

    result = ask_agent(question)

    return result