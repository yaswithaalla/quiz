import re
import random

def generate_quiz_questions(text, num_questions=5):
    # Split text into sentences
    sentences = re.split(r'(?<=[.!?]) +', text)
    questions = []

    for sentence in sentences:
        # Extract words longer than 3 characters (to avoid trivial blanks)
        words = [word for word in re.findall(r'\b\w+\b', sentence) if len(word) > 3]
        if words:
            # Pick a random word to blank out
            chosen_word = random.choice(words)
            # Replace only the first occurrence with a blank
            question = sentence.replace(chosen_word, "_____", 1)
            correct_answer = chosen_word
            questions.append((question, correct_answer))

        if len(questions) >= num_questions:
            break

    return questions

# Example usage
text = """Python is a powerful programming language. It is widely used for web development. Many developers enjoy its simplicity."""
quiz = generate_quiz_questions(text, 3)
for i, (q, a) in enumerate(quiz, 1):
    print(f"Q{i}: {q}")
    print(f"Answer: {a}")
    print()
