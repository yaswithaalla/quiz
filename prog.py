import streamlit as st
import json
import openai

# Use secrets for secure API key access
openai.api_key = st.secrets["OPENAI_API_KEY"]

@st.cache_data
def fetch_questions(text_content, quiz_level):

    RESPONSE_JSON = {
        "mcqs": [
            {
                "mcq": "multiple choice question1",
                "options": {
                    "a": "choice here1",
                    "b": "choice here2",
                    "c": "choice here3",
                    "d": "choice here4",
                },
                "correct": "correct choice option in the form of a, b, c or d",
            }
        ]
    }

    PROMPT_TEMPLATE = f"""
    Text: {text_content}
    You are an expert in generating MCQ type quiz on the basis of provided content. 
    Given the above text, create a quiz of 3 multiple choice questions keeping difficulty level as {quiz_level}. 
    Make sure the questions are not repeated and check all the questions to be conforming the text as well.
    Make sure to format your response like RESPONSE_JSON below and use it as a guide.
    Ensure to make an array of 3 MCQs referring the following response json.

    RESPONSE_JSON: 
    {RESPONSE_JSON}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": PROMPT_TEMPLATE}],
        temperature=0.3,
        max_tokens=1000,
    )

    content = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(content)
        return parsed.get("mcqs", [])
    except json.JSONDecodeError:
        st.error("Could not parse the response from OpenAI. Please try again.")
        return []

def main():
    st.title("Quiz Generator App")

    text_content = st.text_area("Paste the text content here:")
    quiz_level = st.selectbox("Select quiz level:", ["Easy", "Medium", "Hard"])
    quiz_level_lower = quiz_level.lower()

    if st.button("Generate Quiz"):
        if not text_content.strip():
            st.warning("Please enter some text content.")
            return

        with st.spinner("Generating quiz..."):
            questions = fetch_questions(text_content, quiz_level_lower)

        if not questions:
            st.error("Failed to generate questions.")
            return

        st.subheader("Quiz")
        selected_options = []
        correct_answers = []

        for i, question in enumerate(questions):
            st.markdown(f"**Q{i+1}: {question['mcq']}**")
            options = list(question["options"].values())
            selected = st.radio(f"Options for Q{i+1}", options, key=f"q{i}")
            selected_options.append(selected)
            correct_answers.append(question["options"][question["correct"]])

        if st.button("Submit"):
            score = 0
            st.subheader("Results")
            for i in range(len(questions)):
                st.markdown(f"**Q{i+1}: {questions[i]['mcq']}**")
                st.write(f"Your answer: {selected_options[i]}")
                st.write(f"Correct answer: {correct_answers[i]}")
                if selected_options[i] == correct_answers[i]:
                    score += 1
            st.success(f"You scored {score} out of {len(questions)}")

if __name__ == "__main__":
    main()

