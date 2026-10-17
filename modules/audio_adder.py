# ==========================================
# 🔊 ใส่เสียงลงในวิดีโอ — รองรับไฟล์เสียง หรือพิมพ์ข้อความเป็นเสียงพากย์
# ==========================================
from moviepy.editor import VideoFileClip, AudioFileClip
from gtts import gTTS
import os
from config import config

class AudioAdder:
    def __init__(self):
        pass
    
    def text_to_speech(self, text, output_filename="voice.mp3", lang="th"):
        """แปลงข้อความเป็นเสียงพากย์"""
        print(f"🔊 กำลังสร้างเสียงพากย์: {text[:30]}...")
        
        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            output_path = os.path.join(config.OUTPUT_DIR, output_filename)
            tts.save(output_path)
            print(f"✅ เสียงพากย์เสร็จ: {output_path}")
            return {"success": True, "path": output_path}
        except Exception as e:
            print(f"❌ ผิดพลาด: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def add_audio_to_video(self, video_path, audio_source, output_filename="final_video.mp4"):
        """นำเสียงไปต่อกับวิดีโอ"""
        print(f"🔊 กำลังรวมเสียงกับวิดีโอ...")
        
        try:
            video = VideoFileClip(video_path)
            
            # ถ้า audio_source เป็นข้อความ ให้แปลงเป็นเสียงก่อน
            if isinstance(audio_source, str) and audio_source.endswith(".mp3"):
                audio = AudioFileClip(audio_source)
            else:
                tts_result = self.text_to_speech(str(audio_source), "temp_voice.mp3")
                if not tts_result["success"]:
                    return tts_result
                audio = AudioFileClip(tts_result["path"])
            
            # ปรับความยาวเสียงให้ตรงกับวิดีโอ
            if audio.duration > video.duration:
                audio = audio.subclip(0, video.duration)
            
            final_video = video.set_audio(audio)
            output_path = os.path.join(config.OUTPUT_DIR, output_filename)
            final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
            
            video.close()
            audio.close()
            
            print(f"✅ วิดีโอพร้อมเสียงเสร็จสมบูรณ์: {output_path}")
            return {"success": True, "path": output_path}
            
        except Exception as e:
            print(f"❌ ผิดพลาด: {str(e)}")
            return {"success": False, "error": str(e)}

# ทดสอบ
if __name__ == "__main__":
    adder = AudioAdder()
    adder.text_to_speech("สู้ๆ นะครับ! สู้ๆ")

