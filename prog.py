import streamlit as st
import re
import random

st.title("Quiz Question Generator")

# Text input or upload
uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
text_input = st.text_area("Or paste your text here:", height=250)

def generate_quiz_questions(text, num_questions=5):
    sentences = re.split(r'(?<=[.!?]) +', text)
    questions = []

    for sentence in sentences:
        words = [word for word in re.findall(r'\b\w+\b', sentence) if len(word) > 3]
        if words:
            chosen_word = random.choice(words)
            question = sentence.replace(chosen_word, "_____", 1)
            correct_answer = chosen_word
            questions.append((question, correct_answer))

        if len(questions) >= num_questions:
            break

    return questions

# Load text from file or input
main_text = ""
if uploaded_file:
    main_text = uploaded_file.read().decode("utf-8")
elif text_input:
    main_text = text_input

if main_text:
    st.subheader("Loaded Text Preview")
    st.text(main_text[:800] + ("..." if len(main_text) > 800 else ""))

    num_q = st.slider("Number of quiz questions", min_value=1, max_value=10, value=5)
    
    if st.button("Generate Quiz Questions"):
        quiz = generate_quiz_questions(main_text, num_q)
        st.subheader("Quiz Questions")

        quiz_text = ""
        for i, (q, a) in enumerate(quiz, 1):
            st.markdown(f"**Q{i}:** {q}")
            with st.expander("Show Answer"):
                st.write(f"✅ {a}")
            quiz_text += f"Q{i}: {q}\nA: {a}\n\n"

        st.download_button("Download Quiz as Text", quiz_text, file_name="quiz_questions.txt")
else:
    st.info("Please upload a text file or paste your text to generate quiz questions.")

