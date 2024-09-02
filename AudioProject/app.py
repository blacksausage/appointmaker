from flask import Flask, render_template, request, send_from_directory, jsonify
import os
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import time

app = Flask(__name__)

UPLOAD_FOLDER = 'recordings'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check GPU availability
use_gpu = torch.cuda.is_available()
device = "cuda" if use_gpu else "cpu"
torch_dtype = torch.float16 if use_gpu else torch.float32

print(f"Using device: {device}")

# Load model
model_id = "openai/whisper-large-v3"
print("Loading model...")
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

# Create pipeline
pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save-recording', methods=['POST'])
def save_recording():
    if 'audio' not in request.files:
        return 'No audio file', 400
    file = request.files['audio']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'recorded_audio.wav')
        file.save(filename)
        return 'File saved successfully', 200

@app.route('/recordings/<path:filename>')
def serve_audio(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    filename = os.path.join(app.config['UPLOAD_FOLDER'], 'recorded_audio.wav')
    if not os.path.exists(filename):
        return jsonify({"error": "No recorded audio found"}), 400
    
    print(f"Transcribing {filename}...")
    start_time = time.time()
    try:
        result = pipe(filename, batch_size=16 if use_gpu else 4)
        end_time = time.time()
        print(f"Transcription completed in {end_time - start_time:.2f} seconds")
        transcription = result["text"]
        return jsonify({
            "transcription": transcription,
            "time_taken": f"{end_time - start_time:.2f} seconds"
        })
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
