import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from the environment variables
api_key = os.getenv("GoogleAI")

class AIQuestion(BaseModel):
    title: str
    answers: list[str]
    correct_answer: str


questions: list[AIQuestion] = []

def generate_ai_question():
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            #contents='List a few popular cookie recipes. Be sure to include the amounts of ingredients.',
            contents="List one new question about python with 4 answers where one is correct.",
            config={
                'response_mime_type': 'application/json',
                'response_schema': AIQuestion,
            },
        )
        question = response.parsed
        return question
    except Exception as e:
        print(f"Error parsing response: {e}")


def generate_ai_questions(num_questions: int):
    for _ in range(num_questions):
        question = generate_ai_question()
        questions.append(question)
    return questions