import streamlit as st
import tempfile
import os
from faster_whisper import WhisperModel

# تهيئة الموديل
model = WhisperModel("small", device="cpu", compute_type="int8")

st.title("📌 مثابرة تراك - تحليل النطق")
st.write("ارفع تسجيل صوتي (mp3, wav, m4a ...) وهحللهولك 👂")

# رفع ملف الصوت
uploaded_file = st.file_uploader("🎤 ارفع تسجيلك هنا", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    # حفظ الملف مؤقتًا
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        temp_filename = tmp.name

    # تحويل الصوت لنص
    st.info("⏳ جاري التحويل للنص...")
    segments, info = model.transcribe(temp_filename, beam_size=5)
    text = " ".join([seg.text for seg in segments])
    st.success("✅ التحويل خلص")
    st.write("النص المستخرج:")
    st.text(text)

    # ----------------------------
    # التحليل
    # ----------------------------
    feedback = []

    # 1️⃣ كشف التكرار (كلمات)
    words = text.split()
    for i in range(1, len(words)):
        if words[i] == words[i-1]:
            feedback.append(f"🔁 كررت كلمة: '{words[i]}'")

    # 2️⃣ كشف التكرار (حروف)
    for word in words:
        for i in range(1, len(word)):
            if word[i] == word[i-1]:
                feedback.append(f"🔁 كررت حرف '{word[i]}' في كلمة '{word}'")

    # 3️⃣ كشف الاستبدال الشائع
    substitutions = {
        "س": ["ث", "ش"],
        "ر": ["ل", "ي"],
        "غ": ["ق", "ك"]
    }

    for correct, wrong_list in substitutions.items():
        for wrong in wrong_list:
            if wrong in text:
                feedback.append(f"❌ قلت '{wrong}' بدل '{correct}'")

    # عرض الملاحظات
    st.subheader("📊 ملاحظات التحليل")
    if feedback:
        for f in feedback:
            st.warning(f)
    else:
        st.success("👌 النطق سليم (مفيش مشاكل واضحة)")

    # حذف الملف المؤقت
    os.remove(temp_filename)
