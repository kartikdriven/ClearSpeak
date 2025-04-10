from flask import Flask, render_template, request, jsonify
from voice_bot import VoiceBot
import os
import json
import wave
from vosk import Model, KaldiRecognizer
import tempfile
import subprocess

app = Flask(__name__)

# Initialize voice bot and model once
bot = VoiceBot()
model = Model("model")  # Path to Vosk model directory

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'audio' not in request.files:
        return "No audio file uploaded", 400

    audio_file = request.files['audio']

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_webm:
        audio_file.save(temp_webm.name)
        webm_path = temp_webm.name

    # Convert to WAV using ffmpeg
    wav_path = webm_path.replace(".webm", ".wav")
    try:
        result = subprocess.run([
            'ffmpeg', '-y', '-loglevel', 'debug',
            '-i', webm_path,
            '-ar', '16000',
            '-ac', '1',
            '-f', 'wav',
            '-acodec', 'pcm_s16le',
            wav_path
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print("🎥 FFmpeg Output:", result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print("❌ FFmpeg Error:", e.stderr.decode())
        return f"FFmpeg conversion error: {e.stderr.decode()}", 500

    # Validate file size
    size = os.path.getsize(wav_path)
    print(f"🎧 WAV file size: {size} bytes")
    if size < 10000:
        print("🚨 WAV file too small. Likely silent or corrupt.")
        return jsonify({
            'original': "",
            'corrected': "",    
            'feedback': "⚠️ Audio too short or silent. Please try again.",
            'audio_path': ""
        })

    # Save converted WAV permanently to recordings/
    recording_dir = "recordings"
    os.makedirs(recording_dir, exist_ok=True)

    final_output_path = os.path.join(recording_dir, "output.wav")
    os.replace(wav_path, final_output_path)

    # Transcribe with Vosk
    wf = wave.open(final_output_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())

    text = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text += result.get("text", "") + " "
    # 🧠 Don't forget to get final leftover transcription
    final_result = json.loads(rec.FinalResult())
    text += final_result.get("text", "")

    wf.close()

    print("🧠 Transcribed Text:", text)
    text = text.strip()

    if not text:
        print("🚨 No speech recognized.")
        return jsonify({
            'original': "",
            'corrected': "",
            'feedback': "⚠️ Could not recognize any speech. Try speaking clearly and check mic settings.",
            'audio_path': ""
        })

    # Analyze and respond
    corrected_text, feedback, audio_filename = bot.process_audio(text)

    return jsonify({
        'original': text,
        'corrected': corrected_text,
        'feedback': feedback,
        'audio_path': '/' + audio_filename.replace("\\", "/")
    })

if __name__ == '__main__':
    app.run(debug=True)
