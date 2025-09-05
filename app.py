import streamlit as st

st.title("تطبيق مثابرة تراك")
st.write("السلام عليكم ورحمة الله وبركاتة 👋،  Streamlit")
import streamlit as st
from pydub import AudioSegment
import os

st.title("مثابرة تراك - للتخاطب")
st.write("ارفع ملف صوتي هنا:")

uploaded_file = st.file_uploader("اختر ملف صوتي", type=["wav", "mp3", "m4a", "amr"])

if uploaded_file is not None:
    st.success(f"تم رفع الملف: {uploaded_file.name}")
    # حفظ الملف مؤقت
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # تحويل ل wav باستخدام pydub + ffmpeg
    try:
        sound = AudioSegment.from_file(uploaded_file.name)
        out_file = "output.wav"
        sound.export(out_file, format="wav")
        st.audio(out_file)
        st.success("تم التحويل والتشغيل بنجاح ✅")
    except Exception as e:
        st.error(f"خطأ أثناء التحويل: {e}")
