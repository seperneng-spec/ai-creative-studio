# ============================================================
# 🤖 AI CREATIVE STUDIO — ALL-IN-ONE COMPLETE CODE
# สร้างภาพ · ลบพื้นหลัง · ทำให้ขยับได้ · ใส่เสียง — ครบในไฟล์เดียว
# ============================================================

import os
import sys
import requests
import base64
import cv2
import numpy as np
from dotenv import load_dotenv
from PIL import Image
from rembg import remove
from moviepy.editor import VideoFileClip, AudioFileClip
from gtts import gTTS

# ============================================================
# ⚙️ CONFIGURATION — ตั้งค่า
# ============================================================
load_dotenv()

class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    INPUT_DIR = os.path.join(BASE_DIR, "input")
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")
    
    for folder in [INPUT_DIR, OUTPUT_DIR]:
        os.makedirs(folder, exist_ok=True)
    
    IMAGE_GEN_API_URL = os.getenv("IMAGE_GEN_API_URL", "https://api.openai.com/v1/images/generations")
    IMAGE_GEN_API_KEY = os.getenv("IMAGE_GEN_API_KEY", "")
    
    DEFAULT_SIZE = "1024x1024"
    ANIMATION_DURATION = 3
    FPS = 12

config = Config()

# ============================================================
# 🎨 MODULE 1: IMAGE GENERATOR — สร้างภาพด้วย AI
# ============================================================
class ImageGenerator:
    def __init__(self):
        self.api_url = config.IMAGE_GEN_API_URL
        self.api_key = config.IMAGE_GEN_API_KEY
    
    def generate(self, prompt, style="sticker"):
        style_prompts = {
            "sticker": ", sticker style, thick white border, transparent background, no shadows",
            "illustration": ", clean illustration, isolated, transparent background",
            "chibi": ", cute chibi, big eyes, friendly, transparent background"
        }
        full_prompt = prompt + style_prompts.get(style, ", transparent background")
        
        print(f"\n🎨 [1/4] กำลังสร้างภาพ...")
        print(f"    Prompt: {full_prompt[:80]}...")
        
        try:
            if self.api_key and self.api_key != "":
                return self._call_api(full_prompt)
            else:
                return self._demo_mode(full_prompt)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _call_api(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {"prompt": prompt, "n": 1, "size": config.DEFAULT_SIZE, "response_format": "b64_json"}
        resp = requests.post(self.api_url, headers=headers, json=data, timeout=60)
        result = resp.json()
        
        if "data" in result:
            img_data = base64.b64decode(result["data"][0]["b64_json"])
            out_path = os.path.join(config.OUTPUT_DIR, "01_generated.png")
            with open(out_path, "wb") as f:
                f.write(img_data)
            print(f"    ✅ ภาพสร้างเสร็จ")
            return {"success": True, "path": out_path}
        return {"success": False, "error": str(result)}
    
    def _demo_mode(self, prompt):
        return {
            "success": True,
            "mode": "demo",
            "prompt": prompt,
            "note": "📋 คัดลอก Prompt ด้านล่างไปใช้กับ AI เช่น DALL-E, Midjourney"
        }

# ============================================================
# 🧹 MODULE 2: BACKGROUND REMOVER — ลบพื้นหลัง
# ============================================================
class BackgroundRemover:
    def remove(self, input_path):
        print(f"\n🧹 [2/4] กำลังลบพื้นหลัง...")
        try:
            img = Image.open(input_path)
            img_no_bg = remove(img)
            out_path = os.path.join(config.OUTPUT_DIR, "02_no_background.png")
            img_no_bg.save(out_path, format="PNG")
            print(f"    ✅ ลบพื้นหลังเสร็จ")
            return {"success": True, "path": out_path}
        except Exception as e:
            return {"success": False, "error": str(e)}

# ============================================================
# 🎬 MODULE 3: IMAGE ANIMATOR — ทำให้ภาพขยับได้
# ============================================================
class ImageAnimator:
    def animate(self, image_path, style="gentle"):
        print(f"\n🎬 [3/4] กำลังสร้างภาพเคลื่อนไหว...")
        try:
            img = Image.open(image_path).convert("RGBA")
            w, h = img.size
            w2 = ((w + 1) // 2) * 2
            h2 = ((h + 1) // 2) * 2
            img = img.resize((w2, h2))
            img_np = np.array(img)
            
            out_path = os.path.join(config.OUTPUT_DIR, "03_animated.mp4")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video = cv2.VideoWriter(out_path, fourcc, config.FPS, (w2, h2))
            
            total_frames = config.ANIMATION_DURATION * config.FPS
            
            for i in range(total_frames):
                t = i / total_frames
                canvas = np.zeros((h2, w2, 3), dtype=np.uint8)
                
                if style == "gentle":
                    ox = int(np.sin(t * np.pi * 2) * 8)
                    oy = int(np.cos(t * np.pi * 2) * 5)
                elif style == "bounce":
                    ox = 0
                    oy = int(abs(np.sin(t * np.pi * 2)) * 15)
                elif style == "pulse":
                    ox = oy = 0
                    scale = 1 + np.sin(t * np.pi * 2) * 0.03
                    ws, hs = int(w2*scale), int(h2*scale)
                    fr = np.array(img.resize((ws, hs)))
                    xo, yo = (w2-ws)//2, (h2-hs)//2
                    canvas[yo:yo+hs, xo:xo+ws] = fr[:, :, :3]
                    video.write(canvas)
                    continue
                else:
                    ox = oy = 0
                
                x1, y1 = max(0, ox), max(0, oy)
                x2, y2 = min(w2, w2+ox), min(h2, h2+oy)
                xo1, yo1 = max(0, -ox), max(0, -oy)
                xo2, yo2 = min(w2, w2-ox), min(h2, h2-oy)
                canvas[y1:y2, x1:x2] = img_np[yo1:yo2, xo1:xo2, :3]
                video.write(canvas)
            
            video.release()
            print(f"    ✅ ภาพเคลื่อนไหวเสร็จ")
            return {"success": True, "path": out_path}
        except Exception as e:
            return {"success": False, "error": str(e)}

# ============================================================
# 🔊 MODULE 4: AUDIO ADDER — ใส่เสียงลงวิดีโอ
# ============================================================
class AudioAdder:
    def text_to_speech(self, text, lang="th"):
        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            out_path = os.path.join(config.OUTPUT_DIR, "temp_voice.mp3")
            tts.save(out_path)
            return {"success": True, "path": out_path}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def add_audio(self, video_path, voice_text):
        print(f"\n🔊 [4/4] กำลังใส่เสียงพากย์...")
        try:
            video = VideoFileClip(video_path)
            tts_res = self.text_to_speech(voice_text)
            if not tts_res["success"]:
                return tts_res
            
            audio = AudioFileClip(tts_res["path"])
            if audio.duration > video.duration:
                audio = audio.subclip(0, video.duration)
            
            final = video.set_audio(audio)
            out_path = os.path.join(config.OUTPUT_DIR, "04_final_video.mp4")
            final.write_videofile(out_path, codec="libx264", audio_codec="aac", logger=None)
            
            video.close()
            audio.close()
            os.remove(tts_res["path"])
            
            print(f"    ✅ วิดีโอพร้อมเสียงเสร็จสมบูรณ์!")
            return {"success": True, "path": out_path}
        except Exception as e:
            return {"success": False, "error": str(e)}

# ============================================================
# 🚀 MAIN PROGRAM — รวมทุกฟังก์ชัน
# ============================================================
class AICreativeStudio:
    def __init__(self):
        self.generator = ImageGenerator()
        self.bg_remover = BackgroundRemover()
        self.animator = ImageAnimator()
        self.audio_adder = AudioAdder()
        print("=" * 60)
        print("🤖  AI CREATIVE STUDIO — พร้อมใช้งาน")
        print("=" * 60)
    
    def run(self, prompt, voice_text=None, style="sticker", anim_style="gentle", input_image=None):
        results = {}
        img_path = input_image
        
        # Step 1: Generate or Use Provided Image
        if not img_path:
            gen_res = self.generator.generate(prompt, style)
            results["generate"] = gen_res
            if not gen_res["success"]:
                print(f"❌ ผิดพลาด: {gen_res.get('error')}")
                return results
            if gen_res.get("mode") == "demo":
                print("\n" + "=" * 60)
                print(gen_res["note"])
                print(f"\n📝 PROMPT:\n{gen_res['prompt']}")
                print("=" * 60)
                print("\n💡 เมื่อมีรูปแล้ว ให้ใส่รูปในโฟลเดอร์ input/ แล้วใช้ตัวเลือก 'ใช้รูปที่มีอยู่'")
                return results
            img_path = gen_res["path"]
        
        # Step 2: Remove Background
        bg_res = self.bg_remover.remove(img_path)
        results["no_bg"] = bg_res
        if not bg_res["success"]: return results
        
        # Step 3: Animate
        anim_res = self.animator.animate(bg_res["path"], anim_style)
        results["animate"] = anim_res
        if not anim_res["success"]: return results
        
        # Step 4: Add Audio
        if voice_text:
            audio_res = self.audio_adder.add_audio(anim_res["path"], voice_text)
            results["final"] = audio_res
        else:
            results["final"] = anim_res
            print("\n🔊 [4/4] ข้าม — ไม่ได้ระบุข้อความเสียง")
        
        # Summary
        print("\n" + "=" * 60)
        print("✅ 🎉 กระบวนการทั้งหมดเสร็จสมบูรณ์!")
        print("=" * 60)
        for k, v in results.items():
            if isinstance(v, dict) and v.get("success"):
                print(f"  📄 {k}: {os.path.basename(v['path'])}")
        print(f"\n📂 ดูไฟล์ทั้งหมดในโฟลเดอร์: {config.OUTPUT_DIR}")
        return results


# ============================================================
# 🏃‍♂️ เริ่มทำงาน — แก้ตรงนี้ตามต้องการ
# ============================================================
if __name__ == "__main__":
    studio = AICreativeStudio()
    
    # ==============================
    # 📝 ตั้งค่าสำหรับงานของคุณ
    # ==============================
    CONFIG = {
        "prompt": "ชายหนุ่มชุดเกราะสีน้ำเงินลายมังกร ยิ้มแย้มแจ่มใส ยื่นมือทักทาย สไตล์จิบิ",
        "voice_text": "สู้ๆ นะครับ! ทุกคนทำได้แน่นอน สู้ๆ",
        "style": "sticker",        # sticker / chibi / illustration
        "anim_style": "gentle",    # gentle / bounce / pulse
        "input_image": None        # ใส่ path รูปเองได้ เช่น "input/my_pic.png"
    }
    
    # ตรวจสอบว่ามีรูปใน input หรือไม่
    input_pic = os.path.join(config.INPUT_DIR, "input.png")
    if os.path.exists(input_pic):
        print(f"🖼️  พบรูปในโฟลเดอร์ input/ — จะใช้รูปนี้แทนการสร้างใหม่")
        CONFIG["input_image"] = input_pic
    
    # เริ่มทำงาน
    studio.run(
        prompt=CONFIG["prompt"],
        voice_text=CONFIG["voice_text"],
        style=CONFIG["style"],
        anim_style=CONFIG["anim_style"],
        input_image=CONFIG["input_image"]
    )

