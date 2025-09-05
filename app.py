import streamlit as st
from faster_whisper import WhisperModel
import tempfile

st.title("تطبيق مثابرة تراك 🎤")
st.write("السلام عليكم ورحمة الله وبركاتة 👋، Streamlit")

uploaded_file = st.file_uploader("📂 ارفع ملف صوتي", type=["wav", "mp3", "m4a", "ogg"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        temp_wav = tmp.name

    # تفريغ الكلام باستخدام Whisper
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(temp_wav, beam_size=5)

    text = " ".join([segment.text for segment in segments])
    st.subheader("📝 النص المكتشف:")
    st.write(text)

    # كشف الأخطاء البسيطة (بدل الحروف)
    mistakes = []
    if "ث" in text:
        mistakes.append("تم نطق السين كثاء (ث بدل س)")
    if "ش" in text:
        mistakes.append("تم نطق السين كـ ش")
    if "ي" in text or "ل" in text:
        mistakes.append("احتمال استبدال الراء (ر) بـ ي/ل")
    if "غ" in text:
        mistakes.append("احتمال استبدال الراء (ر) بـ غ")

    if mistakes:
        st.subheader("🚨 ملاحظات على النطق:")
        for m in mistakes:
            st.write("- " + m)

    # 🔹 كشف التوقفات (الصمت)
    # silent_ranges = silence.detect_silence(audio, min_silence_len=700, silence_thresh=audio.dBFS-16)

      
            
    else:
        st.write("✅ لا يوجد توقفات طويلة ملحوظة.")
