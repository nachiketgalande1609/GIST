import os
import random
import string
from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from gtts import gTTS
import librosa
from decorators_func import user_required
import requests
from database import AudioFile, db
import matplotlib
matplotlib.use('Agg')

vocab_bp = Blueprint('vocab', __name__)

@vocab_bp.route('/vocab')
@login_required
@user_required
def vocab():

    # COMMENTED FOR DEMO

    # words = ['eat', 'drink', 'water', 'milk', 'cup']
    # word = random.choice(words)
    # headers = {
    #     'Authorization': 'UFUD1Sf8ucQPKBrW8sBnnN5VivqqsHyjhtQqg7aWXWFAfg7XvfpDON7O'
    # }

    # # Fetch image for the main word
    # word_query = f'https://api.pexels.com/v1/search?query={word}&per_page=1'
    # word_response = requests.get(word_query, headers=headers)
    # if word_response.status_code == 200:
    #     word_data = word_response.json()
    #     if 'photos' in word_data and len(word_data['photos']) > 0:
    #         word_url = word_data['photos'][0]['src']['original']
    #     else:
    #         word_url = None
    # else:
    #     word_url = None
    
    word = 'Eat'
    word_url = '../static/images/eating.gif'
    audio_file = f"{word}.wav"
    text_to_audio(word, audio_file)
    plot_file = generate_waveform_plot(audio_file)
    os.remove(audio_file)
    return render_template('vocab.html', word=word, main_word_url=word_url, plot_url=plot_file)

def text_to_audio(word, audio_file):
    tts = gTTS(word)
    tts.save(audio_file)

@vocab_bp.route('/generate-waveform-plot')
@login_required
@user_required
def generate_waveform_plot_route():
    audio_file = request.args.get('audio_file')  # Get the audio file path from the request
    plot_url = generate_waveform_plot_user(audio_file)
    return jsonify({'plot_url': plot_url})

def generate_waveform_plot_user(audio_file):
    import os
    import librosa
    import matplotlib.pyplot as plt
    import soundfile as sf  # Importing soundfile library for audio file reading

    # Construct the full path to the audio file
    audio_path = os.path.join('recordings', audio_file)
    
    try:
        # Attempt to load the audio file using soundfile library
        y, sr = sf.read(audio_path, dtype='float32')
    except Exception as e:
        print(f"Error reading audio file: {e}")
        return None
    
    # Generate waveform plot
    time = librosa.times_like(y)
    plt.figure(figsize=(10, 4))
    plt.plot(time, y)

    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
    plt.axis('off')
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    # Save the plot to a temporary file
    plot_dir = "static/user_plot/"
    os.makedirs(plot_dir, exist_ok=True)

    # Save the plot to the directory
    plot_filename = os.path.splitext(audio_file)[0] + ".png"
    plot_path = os.path.join(plot_dir, plot_filename)
    plt.savefig(plot_path)
    plt.close()
    
    return plot_path

def generate_waveform_plot(audio_file):
    import matplotlib.pyplot as plt
    y, sr = librosa.load(audio_file)
    time = librosa.times_like(y)
    plt.figure(figsize=(10, 4))
    plt.plot(time, y)

    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

    plt.axis('off')
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    # Save the plot to a temporary file
    plot_dir = "static/plot/"
    os.makedirs(plot_dir, exist_ok=True)

    # Save the plot to the directory
    plot_path = os.path.join(plot_dir, os.path.basename(audio_file) + ".png")
    plt.savefig(plot_path)
    plt.close()
    return plot_path

def generate_random_string(length):
    """Generate a random string of letters and digits."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@vocab_bp.route('/save-audio', methods=['POST'])
@login_required
@user_required
def save_audio():
    user_id = current_user.id
    if not user_id:
        return 'User ID not provided in headers', 400
    if 'audio' not in request.files:
        return 'Audio file not provided', 400

    audio_file = request.files['audio']
    filename = f"{user_id}_{generate_random_string(6)}.wav"  # Change extension to WAV
    filepath = 'recordings/' + filename

    # If file already exists, append a number
    index = 1
    while os.path.exists(filepath):
        index += 1
        filename = f"{user_id}_{index}_{generate_random_string(6)}.wav"  # Change extension to WAV
        filepath = 'recordings/' + filename

    # Save the audio file
    audio_file.save(filepath)

    new_audio = AudioFile(user_id=user_id, filepath=filepath)
    db.session.add(new_audio)
    db.session.commit()

    return jsonify({'filename': filename}), 200

