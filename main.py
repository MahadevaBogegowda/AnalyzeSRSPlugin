from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import docx

app = FastAPI()

@app.post("/analyze-srs")
async def analyze_srs(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".docx"):
            raise HTTPException(status_code=400, detail="Only .docx files are supported")

        # Read and parse the DOCX file using python-docx
        doc = docx.Document(file.file)
        full_text = "\n".join([para.text for para in doc.paragraphs])

        # Return the extracted text (you can replace with your actual logic)
        return {"extracted_text": full_text}

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Unexpected error occurred: {str(e)}"})
