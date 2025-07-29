from fastapi import FastAPI, File, UploadFile
import openai
import tempfile
import os
import docx2txt
import textract

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/analyze-srs")
async def analyze_srs(file: UploadFile = File(...)):
    file_ext = file.filename.lower().split('.')[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        if file_ext == "docx":
            text = docx2txt.process(tmp_path)
        elif file_ext in ["pdf", "txt", "xlsx"]:
            text = textract.process(tmp_path).decode("utf-8")
        else:
            return {"error": "Unsupported file format"}

        # Limit input length
        text = text[:3000]

        prompt = (
            "You are a business analyst. Convert the following software requirements "
            "into Agile user stories using this format:\n"
            "As a <user>, I want to <action>, so that <goal>.\n\n"
            f"Requirements:\n{text}"
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=600
        )

        return {"userStories": response.choices[0].message.content.strip()}
    
    finally:
        os.remove(tmp_path)
