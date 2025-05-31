
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from parser import extract_order_data, extract_batch
from pdf_generator import generate_all_pdfs
from supabase_client import store_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process/")
async def process_files(
    order_file: UploadFile,
    pick_file: UploadFile,
    license_plate: str = Form(...),
    analysis_data: str = Form(...)
):
    order_info = extract_order_data(await order_file.read())
    batch = extract_batch(await pick_file.read())
    pdfs = generate_all_pdfs(order_info, batch, analysis_data, license_plate)
    store_data(order_info, batch, analysis_data, license_plate)
    return {"status": "ok", "files": pdfs}
