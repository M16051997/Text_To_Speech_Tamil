from flask import Flask, request, Response
from pydantic import BaseModel
import subprocess
import tempfile
import shutil
import os
import io
from clean_text import translate_numerals_to_words, remove_spaces_and_hyphens

app = Flask(__name__)

# Constants
MODEL_PATH = r"F:\Text Translation Tamil\ta\ta\fastpitch\best_model.pth"
CONFIG_PATH = r"F:\Text Translation Tamil\ta\ta\fastpitch\config.json"
SPEAKERS_FILE_PATH = r"F:\Text Translation Tamil\ta\ta\fastpitch\speakers.pth"
out_path = r"F:\Text Translation Tamil\audio_files"

# Define a Pydantic model to handle input data
class TTSRequest(BaseModel):
    text: str
    speaker_idx: str = "female"

# Define a function to run TTS and return audio data
def run_tts(text, speaker_idx="female"):
    try:
        # Preprocess the text
        clean_text = remove_spaces_and_hyphens(text)
        clean_text = translate_numerals_to_words(clean_text)

        # Create a temporary directory to store the audio file
        temp_dir = tempfile.mkdtemp()
        out_audio_path = os.path.join(temp_dir, "output_audio.wav")

        # Construct the command
        command = [
            "tts",  # Remove the "!" at the beginning
            f'--text "{clean_text}"',
            f'--model_path "{MODEL_PATH}"',
            f'--config_path "{CONFIG_PATH}"',
            f'--out_path "{out_audio_path}"',
            f'--speakers_file_path "{SPEAKERS_FILE_PATH}"',
            f'--speaker_idx "{speaker_idx}"'
        ]

        # Join the command elements into a single string
        command_str = " ".join(command)

        # Run the TTS command using subprocess
        subprocess.run(command_str, shell=True, check=True)
        print("TTS completed successfully.")

        # Read the generated audio data
        with open(out_audio_path, "rb") as audio_file:
            audio_data = audio_file.read()

        # Clean up temporary directory
        shutil.rmtree(temp_dir)

        return audio_data

    except subprocess.CalledProcessError as e:
        print("Error while running TTS:", e)
        return None

# Create an API endpoint to perform TTS using POST
@app.route("/tts/", methods=["POST"])
def tts_endpoint():
    data = request.get_json()
    request_data = TTSRequest(**data)
    audio_data = run_tts(request_data.text, request_data.speaker_idx)

    if audio_data:
        return Response(audio_data, content_type="audio/wav")
    else:
        return {"error": "TTS failed"}

# Create an API endpoint to perform TTS using GET
@app.route("/tts/", methods=["GET"])
def tts_get_endpoint():
    text = request.args.get("text")
    speaker_idx = request.args.get("speaker_idx", "female")
    audio_data = run_tts(text, speaker_idx)

    if audio_data:
        return Response(audio_data, content_type="audio/wav")
    else:
        return {"error": "TTS failed"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
