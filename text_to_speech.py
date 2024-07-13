
from io import BytesIO
from flask_login import login_required
from decorators_func import user_required
import threading
from flask import Blueprint, jsonify, request
from gtts import gTTS
import pygame
from generate import create_sys_msg, generate_response

tts_bp = Blueprint('tts', __name__)

@tts_bp.route('/text_to_speech', methods=['POST'])
@login_required
@user_required
def text_to_speech():
    data = request.get_json()
    text = data.get('text', '')
    module = data.get('module', '')
    if module:
        if module == 'ttm':
            sys_msg = 'You are an assistant who will have a conversation with a child suffering from a speech disorder between the age range of 4 to 8. If the user says a grammatically incorrect statement, start by saying, "Here is a correct way of saying the sentence" and correct the grammar of the sentence. If the user says a grammatically correct sentence, then continue the conversation by asking open ended questions'
        elif module == 'stories':
            sys_msg = 'Tell the user a random short story'
        elif module == 'grammar':
            sys_msg = 'Start by saying "Here is the corrected sentence" and correct the grammatical errors'
        else:
            sys_msg = ''
        messages = create_sys_msg(sys_msg, text)
    else:
        messages = create_sys_msg('', text)
    response = generate_response(messages)
    # Use multithreading to run the generate_speech function in a different thread
    speech_thread = threading.Thread(target=generate_speech, args=(response,))
    speech_thread.start()
    return jsonify({'message': response})

speaking_in_progress = False

# Route for text-to-speech
@tts_bp.route('/speak', methods=['POST'])
@login_required
@user_required
def speak():
    global speaking_in_progress
    if speaking_in_progress:
        return jsonify({'message': 'Speech synthesis already in progress'}), 400
    data = request.get_json()
    text = data.get('text', '')
    speaking_in_progress = True
    generate_speech(text)
    speaking_in_progress = False
    return jsonify({'message': 'Speaking completed'})

def generate_speech(text):
    tts = gTTS(text=text, lang='en')
    speech = BytesIO()
    tts.write_to_fp(speech)
    speech.seek(0)
    
    pygame.mixer.init()
    pygame.mixer.music.load(speech)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)