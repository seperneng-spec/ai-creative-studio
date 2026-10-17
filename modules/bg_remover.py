# ==========================================
# 🧹 ลบพื้นหลังภาพอัตโนมัติ
# ==========================================
from rembg import remove
from PIL import Image
import os
from config import config

class BackgroundRemover:
    def __init__(self):
        pass
    
    def remove(self, input_path, output_filename="no_bg.png"):
        """ลบพื้นหลัง รับไฟล์ภาพ คืนไฟล์ภาพโปร่งใส"""
        
        print(f"🧹 กำลังลบพื้นหลัง: {input_path}")
        
        try:
            # เปิดภาพ
            input_img = Image.open(input_path)
            
            # ลบพื้นหลัง
            output_img = remove(input_img)
            
            # บันทึก
            output_path = os.path.join(config.OUTPUT_DIR, output_filename)
            output_img.save(output_path, format="PNG")
            
            print(f"✅ ลบพื้นหลังเสร็จ: {output_path}")
            return {"success": True, "path": output_path}
            
        except Exception as e:
            print(f"❌ ผิดพลาด: {str(e)}")
            return {"success": False, "error": str(e)}

# ทดสอบ
if __name__ == "__main__":
    remover = BackgroundRemover()
    test_path = os.path.join(config.INPUT_DIR, "test.png")
    if os.path.exists(test_path):
        remover.remove(test_path)

