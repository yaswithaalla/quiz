import streamlit as st
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env if exists
load_dotenv()

# Initialize OpenAI client with API key from environment or Streamlit secrets
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("OpenAI API key not found! Please set OPENAI_API_KEY environment variable or add to Streamlit secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

@st.cache_data
def fetch_questions(text_content, quiz_level):
    RESPONSE_JSON = {
      "mcqs" : [
        {
            "mcq": "multiple choice question1",
            "options": {
                "a": "choice here1",
                "b": "choice here2",
                "c": "choice here3",
                "d": "choice here4",
            },
            "correct": "a",
        },
        {
            "mcq": "multiple choice question2",
            "options": {
                "a": "choice here1",
                "b": "choice here2",
                "c": "choice here3",
                "d": "choice here4",
            },
            "correct": "b",
        },
        {
            "mcq": "multiple choice question3",
            "options": {
                "a": "choice here1",
                "b": "choice here2",
                "c": "choice here3",
                "d": "choice here4",
            },
            "correct": "c",
        }
      ]
    }

    PROMPT_TEMPLATE = f"""
Text: {text_content}
You are an expert in generating MCQ type quiz based on the provided content.
Given the above text, create a quiz of 3 multiple choice questions keeping difficulty level as {quiz_level}.
Make sure the questions are unique and relevant to the text.
Format your response exactly like this JSON example:

{json.dumps(RESPONSE_JSON, indent=2)}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": PROMPT_TEMPLATE}],
        temperature=0.3,
        max_tokens=1000
    )

    content = response.choices[0].message.content
    try:
        data = json.loads(content)
        return data.get("mcqs", [])
    except json.JSONDecodeError:
        st.error("Failed to parse OpenAI response as JSON. Response was:")
        st.code(content)
        return []

def main():
    st.title("Quiz Generator App")

    text_content = st.text_area("Paste the text content here:")

    quiz_level = st.selectbox("Select quiz level:", ["Easy", "Medium", "Hard"])

    if st.button("Generate Quiz"):
        if not text_content.strip():
            st.warning("Please enter some text to generate quiz.")
            return

        questions = fetch_questions(text_content, quiz_level.lower())

        if not questions:
            st.error("No questions generated.")
            return

        selected_options = []
        correct_answers = []

        for question in questions:
            options = [question["options"][key] for key in sorted(question["options"].keys())]
            selected_option = st.radio(question["mcq"], options, key=question["mcq"])
            selected_options.append(selected_option)
            correct_answers.append(question["options"][question["correct"]])

        if st.button("Submit Answers"):
            score = 0
            st.header("Results:")
            for i, question in enumerate(questions):
                st.subheader(f"Q{i+1}: {question['mcq']}")
                st.write(f"Your answer: {selected_options[i]}")
                st.write(f"Correct answer: {correct_answers[i]}")
                if selected_options[i] == correct_answers[i]:
                    score += 1
            st.subheader(f"Your Score: {score} out of {len(questions)}")

if __name__ == "__main__":
    main()


