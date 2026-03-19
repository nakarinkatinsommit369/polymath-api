import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware

# 1. ตั้งค่า Server
app = FastAPI(title="Polymath AI API")

# อนุญาตให้แอปอื่นเข้าถึงได้ (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. ตั้งค่าสมองกล Gemini (ใช้กุญแจที่คุณให้มา)
# แนะนำ: ใน Render ให้ตั้งค่า Environment Variable ชื่อ GEMINI_API_KEY
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCa0426Uu3cKVZ3j75On3k2QZCfL8UQlDI")

# 3. กำหนดรูปแบบการรับข้อมูล (Input)
class IdeaRequest(BaseModel):
    topic: str  # เช่น "ร้านข้าวแกง"
    context: str = "" # ข้อมูลเพิ่มเติม (ถ้ามี)

# 4. ท่อส่งข้อมูลหลัก (The Polymath Engine)
@app.post("/analyze")
async def analyze_idea(request: IdeaRequest):
    try:
model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # นี่คือ "ความรู้เฉพาะทาง" (Master Prompt) ของคุณ
        master_prompt = f"""
        คุณคือ "Universal Polymath" ระดับสูงสุด
        จงชำแหละและสร้างนวัตกรรมใหม่สำหรับหัวข้อ: {request.topic}
        โดยใช้ข้อมูลเพิ่มเติม: {request.context}
        
        โครงสร้างคำตอบ:
        1. First Principles Analysis (แก่นแท้)
        2. Cross-Pollination Idea (ไอเดียผสมข้ามศาสตร์ที่บ้าบิ่น)
        3. The Grand Slam Offer (ข้อเสนอที่ลูกค้าปฏิเสธไม่ได้)
        4. Action Plan (3 ขั้นตอนทำทันที)
        """
        
        response = model.generate_content(master_prompt)
        return {"status": "success", "result": response.text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"message": "Polymath API is running!"}
