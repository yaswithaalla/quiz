import streamlit as st
from transformers import pipeline
from googletrans import Translator
from gtts import gTTS
import tempfile
import os

st.set_page_config(page_title="Quiz & Summary Generator", layout="centered")

summarizer = pipeline("summarization")
qa_pipeline = pipeline("question-answering")
translator = Translator()

st.title("Paragraph Quiz & Summary Generator")

paragraph = st.text_area("Enter a paragraph:", height=300)

lang_map = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Bengali": "bn",
    "Marathi": "mr",
    "Kannada": "kn",
    "Gujarati": "gu",
    "Malayalam": "ml",
    "Punjabi": "pa",
    "Urdu": "ur"
}

target_lang = st.selectbox("Choose output language for summary and speech:", list(lang_map.keys()))
language_code = lang_map[target_lang]

def extract_keywords(text, num=3):
    words = list(set(text.split()))
    return words[:num]

if st.button("Generate Quiz and Summary"):
    if not paragraph.strip():
        st.warning("Please enter a paragraph.")
    else:
        with st.spinner("Summarizing..."):
            summary = summarizer(paragraph, max_length=150, min_length=40, do_sample=False)[0]["summary_text"]

        with st.spinner("Translating summary..."):
            translated = translator.translate(summary, dest=language_code).text
            bullet_points = [f"- {line.strip()}" for line in translated.split(". ") if line.strip()]

        st.subheader("Summary in Bullet Points")
        for point in bullet_points:
            st.markdown(point)

        with st.spinner("Generating quiz questions..."):
            keywords = extract_keywords(paragraph)
            st.subheader("Quiz Questions and Answers")
            for i, keyword in enumerate(keywords):
                question = f"What is {keyword}?"
                answer = qa_pipeline(question=question, context=paragraph)["answer"]
                st.markdown(f"*Q{i+1}: {question}*")
                st.markdown(f"*Answer:* {answer}")

        with st.spinner("Generating speech..."):
            tts = gTTS(text="\n".join(bullet_points), lang=language_code)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name, format="audio/mp3")
                os.unlink(fp.name)

