# ==========================================
# 🎨 สร้างภาพด้วย AI
# ==========================================
import requests
import base64
import os
from config import config

class ImageGenerator:
    def __init__(self):
        self.api_url = config.IMAGE_GEN_API_URL
        self.api_key = config.IMAGE_GEN_API_KEY
    
    def generate(self, prompt, style="sticker"):
        """สร้างภาพจากคำบรรยาย พร้อมเพิ่มคำสั่งไม่มีพื้นหลัง"""
        
        # เพิ่มคำสั่งอัตโนมัติตามสไตล์ที่เลือก
        style_prompts = {
            "sticker": ", sticker style, thick white border, transparent background, no shadows",
            "illustration": ", clean illustration, isolated, transparent background",
            "chibi": ", cute chibi, big eyes, friendly, transparent background"
        }
        
        full_prompt = prompt + style_prompts.get(style, ", transparent background")
        
        print(f"🎨 กำลังสร้างภาพ: {full_prompt[:60]}...")
        
        try:
            # === ถ้ามี API Key จริง ให้ใช้ส่วนนี้ ===
            if self.api_key and self.api_key != "":
                return self._call_openai_api(full_prompt)
            else:
                # === โหมดสาธิต — ส่งคำสั่งให้ผู้ใช้ใช้กับ AI อื่น ===
                return self._demo_mode(full_prompt)
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _call_openai_api(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": prompt,
            "n": 1,
            "size": config.DEFAULT_SIZE,
            "response_format": "b64_json"
        }
        response = requests.post(self.api_url, headers=headers, json=data)
        result = response.json()
        
        if "data" in result:
            image_data = base64.b64decode(result["data"][0]["b64_json"])
            output_path = os.path.join(config.OUTPUT_DIR, "generated.png")
            with open(output_path, "wb") as f:
                f.write(image_data)
            return {"success": True, "path": output_path, "prompt": prompt}
        return {"success": False, "error": str(result)}
    
    def _demo_mode(self, prompt):
        """โหมดสาธิต — แสดง Prompt สำหรับคัดลอกไปใช้กับ AI อื่น"""
        return {
            "success": True,
            "mode": "demo",
            "prompt": prompt,
            "note": "คัดลอก Prompt ด้านล่างไปใช้กับ AI เช่น DALL-E, Midjourney ได้เลยครับ",
            "full_prompt": prompt
        }

# ทดสอบใช้งาน
if __name__ == "__main__":
    gen = ImageGenerator()
    result = gen.generate("ชายหนุ่มชุดเกราะสีน้ำเงิน ยืนยิ้มแย้ม ชูนิ้วโป้ง", style="sticker")
    print("\n✅ Prompt ที่ใช้:")
    print(result.get("full_prompt", result.get("prompt")))

