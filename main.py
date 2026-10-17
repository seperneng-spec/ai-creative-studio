# ==========================================
# 🤖 AI CREATIVE STUDIO — MAIN PROGRAM
# รวมทุกฟังก์ชันไว้ที่นี่: สร้างภาพ → ลบพื้นหลัง → ขยับได้ → มีเสียง
# ==========================================

import os
from config import config
from modules.image_generator import ImageGenerator
from modules.bg_remover import BackgroundRemover
from modules.animator import ImageAnimator
from modules.audio_adder import AudioAdder

class AICreativeStudio:
    def __init__(self):
        self.generator = ImageGenerator()
        self.remover = BackgroundRemover()
        self.animator = ImageAnimator()
        self.audio_adder = AudioAdder()
        
        print("="*60)
        print("🤖 AI CREATIVE STUDIO — พร้อมใช้งาน")
        print("="*60)
    
    def full_pipeline(self, prompt, voice_text=None, style="sticker", animation_style="gentle"):
        """
        🔄 กระบวนการเต็มรูปแบบ
        1. สร้างภาพ → 2. ลบพื้นหลัง → 3. ทำให้ขยับ → 4. ใส่เสียง
        """
        print("\n🚀 เริ่มกระบวนการสร้าง...\n")
        
        results = {}
        
        # ===== ขั้นที่ 1: สร้างภาพ =====
        print("📌 ขั้นที่ 1/4 — สร้างภาพด้วย AI")
        gen_result = self.generator.generate(prompt, style=style)
        results["generated"] = gen_result
        
        if not gen_result.get("success"):
            print("⚠️ ไม่สามารถสร้างภาพได้ — จบการทำงาน")
            return results
        
        if gen_result.get("mode") == "demo":
            print("\n📋 === PROMPT สำหรับคัดลอกไปใช้ ===")
            print(gen_result["full_prompt"])
            print("=================================\n")
            print("💡 คำแนะนำ: นำภาพที่สร้างได้มาใส่ในโฟลเดอร์ input/ แล้วใช้ขั้นตอนที่ 2-4 ต่อได้เลยครับ")
            return results
        
        # ===== ขั้นที่ 2: ลบพื้นหลัง =====
        print("\n📌 ขั้นที่ 2/4 — ลบพื้นหลัง")
        bg_result = self.remover.remove(gen_result["path"], "step2_no_bg.png")
        results["no_background"] = bg_result
        
        if not bg_result["success"]:
            return results
        
        # ===== ขั้นที่ 3: ทำให้ขยับได้ =====
        print("\n📌 ขั้นที่ 3/4 — สร้างภาพเคลื่อนไหว")
        anim_result = self.animator.animate(
            bg_result["path"], 
            "step3_animated.mp4",
            style=animation_style
        )
        results["animated"] = anim_result
        
        if not anim_result["success"]:
            return results
        
        # ===== ขั้นที่ 4: ใส่เสียง =====
        if voice_text:
            print("\n📌 ขั้นที่ 4/4 — ใส่เสียงพากย์")
            audio_result = self.audio_adder.add_audio_to_video(
                anim_result["path"],
                voice_text,
                "step4_final_video.mp4"
            )
            results["final"] = audio_result
        else:
            print("\n📌 ขั้นที่ 4/4 — ข้าม (ไม่ได้ระบุข้อความเสียง)")
            results["final"] = anim_result
        
        # ===== สรุปผล =====
        print("\n" + "="*60)
        print("✅ 🎉 กระบวนการสร้างเสร็จสมบูรณ์!")
        print("="*60)
        for step, res in results.items():
            if isinstance(res, dict) and res.get("success"):
                print(f"  ✅ {step}: {res.get('path', 'เสร็จสิ้น')}")
        
        return results


# ==========================================
# 🏃‍♂️ เริ่มทำงานเมื่อรันไฟล์นี้โดยตรง
# ==========================================
if __name__ == "__main__":
    studio = AICreativeStudio()
    
    # ==============================
    # 📝 ตัวอย่างการใช้งาน — แก้ตรงนี้ได้เลย
    # ==============================
    studio.full_pipeline(
        prompt="ชายหนุ่มชุดเกราะสีน้ำเงินลายมังกร ยิ้มแย้มแจ่มใส ยื่นมือมาทางทักทาย สไตล์การ์ตูนจิบิ",
        voice_text="สู้ๆ นะครับ! ทุกคนทำได้ สู้ๆ",
        style="sticker",           # sticker / chibi / illustration
        animation_style="gentle"   # gentle / bounce / pulse
    )

