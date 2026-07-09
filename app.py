from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
import os
#BACKEND

app = FastAPI(
    title="AI Interview Preparation API",
    version="1.0"
)

# Read API key from environment variable


client=genai.Client(api_key=os.environ["GEMINI_API_KEY"])

class InterviewRequest(BaseModel):
    language: str
    category: str
    difficulty: str
    experience: str
    company: str
    role: str
    count: int
    answer_type: str


@app.get("/")
def home():
    return {
        "message": "AI Interview Preparation API Running Successfully"
    }


@app.post("/generate")
def generate_questions(data: InterviewRequest):

    prompt = f"""
You are an expert technical interviewer.

Generate {data.count} interview questions.

Programming Language:
{data.language}

Interview Category:
{data.category}

Difficulty:
{data.difficulty}

Candidate Experience:
{data.experience}

Target Company:
{data.company}

Job Role:
{data.role}

Output Type:
{data.answer_type}

Instructions:

1. Make the questions suitable for the selected company.

2. Match the difficulty level.

3. Match the candidate's experience.

4. If Output Type is "Questions Only",
return only numbered questions.

5. If Output Type is "Questions + Answers",
return:

Question 1

Answer

Question 2

Answer

Continue until all questions are completed.

6. Do not include unnecessary introductions.

7. Use professional interview questions.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return {
            "status": "success",
            "language": data.language,
            "category": data.category,
            "company": data.company,
            "role": data.role,
            "result": response.text
        }

    except Exception as e:

        return {
            "status": "error",
            "result": str(e)
        }