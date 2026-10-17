
# ==========================================
# 🤖 AI Creative Studio — Configuration
# ==========================================
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # โฟลเดอร์
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    INPUT_DIR = os.path.join(BASE_DIR, "input")
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")
    
    # สร้างโฟลเดอร์ถ้ายังไม่มี
    for folder in [INPUT_DIR, OUTPUT_DIR]:
        os.makedirs(folder, exist_ok=True)
    
    # AI Image Generation API (สามารถเปลี่ยนเป็นบริการอื่นได้)
    IMAGE_GEN_API_URL = os.getenv("IMAGE_GEN_API_URL", "https://api.openai.com/v1/images/generations")
    IMAGE_GEN_API_KEY = os.getenv("IMAGE_GEN_API_KEY", "")
    
    # ค่าเริ่มต้น
    DEFAULT_SIZE = "1024x1024"
    ANIMATION_DURATION = 3  # วินาที
    FPS = 12

config = Config()
