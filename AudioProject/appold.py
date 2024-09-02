from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'recordings'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

if __name__ == '__main__':
    app.run(debug=True)
