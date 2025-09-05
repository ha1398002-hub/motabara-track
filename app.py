import streamlit as st
import whisper

# عنوان التطبيق
st.set_page_config(page_title="تطبيق مثابرة تراك", page_icon="🎤", layout="centered")

st.title("🎤 تطبيق مثابرة تراك")
st.write("السلام عليكم ورحمة الله وبركاته 👋")
st.write("ارفع تسجيل صوتي، والتطبيق هيحوّله إلى نص مكتوب.")

# رفع ملف صوت
uploaded_file = st.file_uploader("📂 ارفع ملف صوت (MP3 أو WAV)", type=["mp3", "wav"])

if uploaded_file is not None:
    # حفظ الملف المرفوع مؤقتًا
    with open("audio_input.mp3", "wb") as f:
        f.write(uploaded_file.read())

    st.info("⏳ جاري تحويل الصوت إلى نص...")

    # تحميل نموذج Whisper
    model = whisper.load_model("base")

    # تحويل الصوت إلى نص
    result = model.transcribe("audio_input.mp3", language="ar")

    # عرض النص
    st.success("✅ النص المستخرج:")
    st.write(result["text"])
