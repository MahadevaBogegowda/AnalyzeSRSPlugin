# ✅ analyze_srs_plugin/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from docx import Document
from io import BytesIO
import openai
import os

app = FastAPI()

# Allow CORS (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set your OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/analyze-srs")
async def analyze_srs(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        print(f"✅ Received file: {file.filename}, size: {len(contents)} bytes")

        # Extract text from .docx file
        try:
            document = Document(BytesIO(contents))
            full_text = "\n".join([para.text for para in document.paragraphs])
        except Exception as e:
            print("❌ Error reading DOCX:", e)
            raise HTTPException(status_code=400, detail="Failed to read DOCX file")

        print("📄 Extracted text length:", len(full_text))

        # Call OpenAI API to generate user stories
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an assistant that writes Agile user stories."},
                    {"role": "user", "content": f"Extract user stories from this SRS:\n\n{full_text}"}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            result = response.choices[0].message.content
        except Exception as e:
            print("❌ GPT error:", e)
            raise HTTPException(status_code=500, detail="AI processing failed")

        return {"user_stories": result.strip()}

    except Exception as e:
        print("❌ General error:", e)
        raise HTTPException(status_code=500, detail="Unexpected error occurred")
