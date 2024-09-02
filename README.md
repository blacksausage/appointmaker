Audio Transcription Project
This project provides a web interface for recording audio and transcribing it using a pre-trained model.

Prerequisites
Python 3.7 or higher
pip (Python package installer)
Ubuntu 20.04 or similar Linux distribution
Installation
Clone this repository or download the project files.

Open a terminal in the project directory.

It's recommended to create a virtual environment:

python3 -m venv venv
source venv/bin/activate
Install the required Python packages:

pip install flask torch transformers
Install system dependencies:

sudo apt update
sudo apt install ffmpeg portaudio19-dev python3-pyaudio
Install additional audio processing libraries:

pip install librosa soundfile
If you're planning to use CUDA for GPU acceleration (optional):

pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
Note: The CUDA version may need to be adjusted based on your system.

Setting up PulseAudio and PipeWire
Ubuntu 20.04 uses PulseAudio by default, but newer versions use PipeWire. If you're having audio issues, you might want to try PipeWire:

Install PipeWire:

sudo apt install pipewire
Replace PulseAudio with PipeWire:

sudo apt install pipewire-audio-client-libraries
systemctl --user --now disable pulseaudio.service pulseaudio.socket
systemctl --user mask pulseaudio
systemctl --user --now enable pipewire-pulse.service
Reboot your system:

sudo reboot
Running the Application
Ensure you're in the project directory and your virtual environment is activated.

Run the Flask application:

python app.py
Open a web browser and navigate to http://localhost:5000.

Troubleshooting
If you encounter issues with your microphone or audio input:

Check available audio sources:

pactl list short sources
Set your desired audio source as default:

pactl set-default-source [source_name]
If using a Bluetooth device, ensure it's in the correct mode:

pactl set-card-profile [card_name] headset-head-unit
Check PipeWire status:

systemctl --user status pipewire pipewire-pulse
If services are not running, start them:

systemctl --user start pipewire pipewire-pulse
For more detailed troubleshooting, please refer to the Ubuntu or PipeWire documentation.

License
[Include your chosen license here]

Acknowledgements
This project uses the following open-source libraries:

Flask
PyTorch
Transformers
Librosa
We thank the developers of these libraries for their contributions to the open-source community.
