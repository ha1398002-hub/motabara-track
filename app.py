import streamlit as st
import whisper

# إعدادات الصفحة
st.set_page_config(page_title="تطبيق مثابرة تراك", page_icon="🎤", layout="centered")

st.title("🎤 تطبيق مثابرة تراك")
st.write("السلام عليكم ورحمة الله وبركاته 👋")
st.write("ارفع أي ملف صوتي، والتطبيق هيحوّله إلى نص مكتوب.")

# رفع ملف صوت (أي نوع)
uploaded_file = st.file_uploader("📂 ارفع ملف صوت (أي صيغة مدعومة)", type=None)

if uploaded_file is not None:
    # حفظ الملف المرفوع مؤقتًا بنفس الامتداد
    filename = "audio_input." + uploaded_file.name.split(".")[-1]
    with open(filename, "wb") as f:
        f.write(uploaded_file.read())

    st.info("⏳ جاري تحويل الصوت إلى نص...")

    # تحميل نموذج Whisper
    model = whisper.load_model("base")

    # تحويل الصوت إلى نص
    result = model.transcribe(filename, language="ar")

    # عرض النص
    st.success("✅ النص المستخرج:")
    st.write(result["text"])
