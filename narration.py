from io import BytesIO
from gtts import gTTS
import pygame

# Text you want to convert to speech
text = '''
    Introducing our groundbreaking platform designed to support children with autism on their journey to communication and learning.

Meet Sarah, a caring mother dedicated to helping her child thrive. With our user-friendly interface, getting started is simple.

Sarah effortlessly signs up, unlocking a world of possibilities for her child.

Now, let's explore the heart of our platform: the vocabulary building feature.

Each card pairs a vivid image with its corresponding word, creating an immersive learning experience.

With just a tap, the platform vocalizes the word, helping children reinforce their auditory skills.

And here's where the magic happens. The record button empowers children to practice and master their speech.

With each repetition, our platform provides gentle guidance and encouragement, fostering confidence and progress.

Join us in revolutionizing the way children with autism learn and communicate. Together, we can unlock a world of possibilities.
'''

tlds = {
    "United States": "com",
    "United Kingdom": "co.uk",
    "Australia": "com.au",
    "Canada": "ca",
    "Ireland": "ie",    
    "India": "co.in",
}

def generate_speech(text):
    tts = gTTS(text=text, tld=tlds["United States"], slow=False)
    speech = BytesIO()
    tts.write_to_fp(speech)
    speech.seek(0)
    
    pygame.mixer.init()
    pygame.mixer.music.load(speech)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

generate_speech(text)