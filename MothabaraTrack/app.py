import streamlit as st
import tempfile, os
from pydub import AudioSegment

st.set_page_config(page_title="مثابرة تراك", layout="wide")
st.title("🎤 مثابرة تراك — تحليل النطق")

st.markdown("ارفع ملف صوتي (mp3 / wav / m4a). التطبيق سيحوّله لصيغة wav ثم يحاول تحويله إلى نص وتحليله.")

uploaded_file = st.file_uploader("ارفع ملف صوتي هنا", type=["wav", "mp3", "m4a", "amr"])

def analyze_text_and_segments(text, segments):
    issues = []
    # تكرار كلمات متتابعة
    words = text.split()
    for i in range(1, len(words)):
        if words[i] == words[i-1]:
            issues.append(f"تكرار كلمة متتابعة: «{words[i]}»")

    # توقفات طويلة باستخدام الـ segments (لو متاح)
    try:
        prev_end = None
        for s in segments:
            start = getattr(s, "start", s.get("start") if isinstance(s, dict) else None)
            end = getattr(s, "end", s.get("end") if isinstance(s, dict) else None)
            if prev_end is not None and start is not None:
                silence = start - prev_end
                if silence > 1.5:
                    issues.append(f"وقفة طويلة قبل جزء عند {start:.2f}s (مدة {silence:.2f}s)")
            prev_end = end
    except Exception:
        pass

    # لَدغات / استبدالات تقريبية (تحليل بسيط نصي)
    if "ث" in text and "س" not in text:
        issues.append("احتمال استبدال السين بالثاء")
    if "ش" in text and "س" not in text:
        issues.append("احتمال استبدال السين بالشين")
    if "ي" in text and "ر" not in text:
        issues.append("احتمال استبدال الراء بالياء")
    if "ل" in text and "ر" not in text:
        issues.append("احتمال استبدال الراء باللام")
    if "غ" in text and "ر" not in text:
        issues.append("احتمال استبدال الراء بالغين")

    # تلعثم حرفي: تكرار نفس الحرف داخل الكلمة (مثال: مـمـم)
    for w in words:
        for ch in set(w):
            if w.count(ch) >= 3:
                issues.append(f"تلعثم/تكرار حرفي داخل كلمة: «{w}» (الحرف «{ch}» تكرر)")

    return issues

if uploaded_file:
    # حفظ مؤقت للملف المرفوع
    suffix = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.success(f"تم رفع الملف: {uploaded_file.name}")
    st.audio(tmp_path)

    # نحاول تحويل أي صيغة إلى WAV (PCM) باستخدام pydub/ffmpeg
    wav_path = tmp_path + ".wav"
    try:
        AudioSegment.from_file(tmp_path).export(wav_path, format="wav")
    except Exception as e:
        st.error("خطأ أثناء تحويل الملف إلى WAV: " + str(e))
        os.remove(tmp_path)
        st.stop()

    st.info("⏳ جاري تحويل الصوت إلى نص (محاولة سريعة)...")

    text = None
    segments = []

    # محاولة استخدام faster-whisper أولاً (لو متاحة)
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("small", device="cpu", compute_type="int8")
        segments_obj, info = model.transcribe(wav_path, beam_size=5)
        # نجمع النص ونحتفظ بالـ segments
        text = " ".join([seg.text.strip() for seg in segments_obj]).strip()
        # نحول segments_obj إلى قائمة dict بسيطة للاستخدام
        for seg in segments_obj:
            segments.append({"start": float(seg.start), "end": float(seg.end), "text": seg.text})
    except Exception as e_fw:
        st.warning("faster-whisper غير متاح أو فشل (سيُحاول استخدام طريقة احتياطية).")
        # محاولة بديلة باستخدام SpeechRecognition + Google (قد ينجح على السحابة)
        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            with sr.AudioFile(wav_path) as source:
                audio_data = r.record(source)
                text = r.recognize_google(audio_data, language="ar-EG")
                segments = [{"start": 0.0, "end": 0.0, "text": text}]
        except Exception as e_sr:
            st.error("لم أستطع تحويل الملف لنص هنا:\n" + str(e_sr))

    if text:
        st.subheader("📄 النص المحوّل:")
        st.write(text)

        st.subheader("🔎 نتيجة التحليل:")
        issues = analyze_text_and_segments(text, segments)
        if issues:
            for it in issues:
                st.warning(it)
        else:
            st.success("لم يتم اكتشاف مشاكل واضحة في النص.")

    # تنظيف ملفات مؤقتة
    try:
        os.remove(tmp_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)
    except:
        pass
