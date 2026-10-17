# ==========================================
# 🎬 ทำให้ภาพนิ่งขยับได้ — สร้างวิดีโอสั้น
# ==========================================
from PIL import Image
import numpy as np
import cv2
import os
from config import config

class ImageAnimator:
    def __init__(self):
        self.duration = config.ANIMATION_DURATION
        self.fps = config.FPS
    
    def animate(self, image_path, output_filename="animated.mp4", style="gentle"):
        """
        ทำให้ภาพขยับได้
        style: gentle = ขยับเบาๆ, bounce = กระเด้ง, pulse = กระพริบ
        """
        print(f"🎬 กำลังสร้างภาพเคลื่อนไหว: {style}")
        
        try:
            img = Image.open(image_path).convert("RGBA")
            width, height = img.size
            
            # ปรับขนาดให้พอดี
            new_w = ((width + 1) // 2) * 2
            new_h = ((height + 1) // 2) * 2
            img = img.resize((new_w, new_h))
            img_np = np.array(img)
            
            output_path = os.path.join(config.OUTPUT_DIR, output_filename)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video = cv2.VideoWriter(output_path, fourcc, self.fps, (new_w, new_h))
            
            total_frames = self.duration * self.fps
            
            for i in range(total_frames):
                progress = i / total_frames
                
                # สร้างเอฟเฟกต์ตามสไตล์
                if style == "gentle":
                    # ขยับซ้าย-ขวาเบาๆ
                    offset_x = int(np.sin(progress * np.pi * 2) * 8)
                    offset_y = int(np.cos(progress * np.pi * 2) * 5)
                elif style == "bounce":
                    # กระเด้งขึ้นลง
                    offset_y = int(abs(np.sin(progress * np.pi * 2)) * 15)
                    offset_x = 0
                elif style == "pulse":
                    # ขยาย-หดเล็กน้อย
                    scale = 1 + np.sin(progress * np.pi * 2) * 0.03
                    offset_x = offset_y = 0
                    
                    # ปรับขนาดตามสเกล
                    w2 = int(new_w * scale)
                    h2 = int(new_h * scale)
                    frame = np.array(Image.fromarray(img_np).resize((w2, h2)))
                    # วางตรงกลาง
                    canvas = np.zeros((new_h, new_w, 3), dtype=np.uint8)
                    x_off = (new_w - w2) // 2
                    y_off = (new_h - h2) // 2
                    canvas[y_off:y_off+h2, x_off:x_off+w2] = frame[:, :, :3]
                    video.write(canvas)
                    continue
                else:
                    offset_x = offset_y = 0
                
                # สร้างเฟรมว่าง
                canvas = np.zeros((new_h, new_w, 3), dtype=np.uint8)
                
                # คำนวณตำแหน่ง
                x1 = max(0, offset_x)
                y1 = max(0, offset_y)
                x2 = min(new_w, new_w + offset_x)
                y2 = min(new_h, new_h + offset_y)
                
                # วางภาพลงเฟรม
                canvas[y1:y2, x1:x2] = img_np[max(0, -offset_y):min(new_h, new_h-offset_y),
                                               max(0, -offset_x):min(new_w, new_w-offset_x), :3]
                
                video.write(canvas)
            
            video.release()
            print(f"✅ สร้างภาพเคลื่อนไหวเสร็จ: {output_path}")
            return {"success": True, "path": output_path}
            
        except Exception as e:
            print(f"❌ ผิดพลาด: {str(e)}")
            return {"success": False, "error": str(e)}

# ทดสอบ
if __name__ == "__main__":
    animator = ImageAnimator()
    test_img = os.path.join(config.OUTPUT_DIR, "no_bg.png")
    if os.path.exists(test_img):
        animator.animate(test_img, style="gentle")

