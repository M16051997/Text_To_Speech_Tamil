from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess

app = FastAPI()

# Define a Pydantic model for the request data
class TextToSpeechRequest(BaseModel):
    text: str
    speaker_idx: str

@app.post("/tts/")
async def run_tts_and_return_audio(request: TextToSpeechRequest):
    try:
        # Paths to model files (update these paths)
        model_path = r"F:\Text Translation Tamil\ta\ta\fastpitch\best_model.pth"
        config_path = r"F:\Text Translation Tamil\ta\ta\fastpitch\config.json"
        speakers_file_path = r"F:\Text Translation Tamil\ta\ta\fastpitch\speakers.pth"
        
        # Construct the command to run the "tts" tool
        command = [
            "tts",
            f'--text "{request.text}"',
            f'--model_path "{model_path}"',
            f'--config_path "{config_path}"',
            f'--speakers_file_path "{speakers_file_path}"',
            f'--speaker_idx "{request.speaker_idx}"'
        ]

        # Join the command elements into a single string
        command_str = " ".join(command)

        # Run the TTS command using subprocess and capture the output
        audio_output = subprocess.check_output(command_str, shell=True)

        # Return the audio data as a response
        return {"audio": audio_output.decode('utf-8')}
    
    except subprocess.CalledProcessError as e:
        # Handle TTS command error
        raise HTTPException(status_code=500, detail=f"TTS failed: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
