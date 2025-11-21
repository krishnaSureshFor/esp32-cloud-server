from fastapi import FastAPI, UploadFile
import requests
import tempfile
from faster_whisper import WhisperModel

app = FastAPI()

# Load Whisper model once
whisper = WhisperModel("tiny")

@app.post("/process_audio")
async def process_audio(file: UploadFile):
    # Save uploaded audio
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp.write(await file.read())
    temp.close()

    # STT with Whisper
    segments, _ = whisper.transcribe(temp.name)
    text = " ".join([s.text for s in segments])
    print("User said:", text)

    # DeepSeek API (FREE)
    res = requests.post(
        "https://api.siliconflow.cn/v1/chat/completions",
        headers={"Authorization": "Bearer sk-ezqdqvjyzfosrykzvjbqsazkyvzazjpmbgikxwkqntqojnuj"},
        json={
            "model": "deepseek-ai/DeepSeek-R1",
            "messages": [{"role": "user", "content": text}]
        },
    )

    reply = res.json()['choices'][0]['message']['content']
    return {"reply": reply}
