from fastapi import FastAPI, UploadFile
import requests
import tempfile

app = FastAPI()

DEEPGRAM_KEY = "4bf84799fe7a1114a3ef16b73d36ab80c720bb94"
DEEPSEEK_KEY = "sk-ezqdqvjyzfosrykzvjbqsazkyvzazjpmbgikxwkqntqojnuj"

@app.post("/process_audio")
async def process_audio(file: UploadFile):
    # Save uploaded file
    audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio_file.write(await file.read())
    audio_file.close()

    # 1️⃣ Convert Audio → Text using Deepgram STT
    with open(audio_file.name, "rb") as f:
        dg_res = requests.post(
            "https://api.deepgram.com/v1/listen?model=nova-2",
            headers={"Authorization": f"Token {DEEPGRAM_KEY}"},
            data=f
        )

    text = dg_res.json()["results"]["channels"][0]["alternatives"][0]["transcript"]
    print("User said:", text)

    # 2️⃣ Text → AI response using DeepSeek
    res = requests.post(
        "https://api.siliconflow.cn/v1/chat/completions",
        headers={"Authorization": f"Bearer {DEEPSEEK_KEY}"},
        json={
            "model": "deepseek-ai/DeepSeek-R1",
            "messages": [{"role": "user", "content": text}]
        }
    )

    reply = res.json()["choices"][0]["message"]["content"]
    return {"reply": reply}
