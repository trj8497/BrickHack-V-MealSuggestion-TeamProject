import io
from playsound import playsound
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\tejas\\Desktop\\Brickhack6\\The_Vision\\Vision Project-9d1350f85714.json"

from pygame import mixer  # Load the popular external library


# def play_mp3(file):
#     mixer.init()
#     mixer.music.load(file)
#     mixer.music.play()

def synthesize_text(text):
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.types.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        name='en-US-Standard-C',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)

    # The response's audio_content is binary.
    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

def detect_landmarks(path):
    """Detects landmarks in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    print('Landmarks:')

    for landmark in landmarks:
        print(landmark.description)
        for location in landmark.locations:
            lat_lng = location.lat_lng
            print('Latitude {}'.format(lat_lng.latitude))
            print('Longitude {}'.format(lat_lng.longitude))
            synthesize_text(landmark.description + ' with ' + 'Latitude {}'.format(lat_lng.latitude) + ' and ' + 'Longitude {}'.format(lat_lng.longitude))
            # print('Longitude {}'.format(lat_lng.longitude))
            # synthesize_text('Longitude {}'.format(lat_lng.longitude))
            playsound('output.mp3')

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

detect_landmarks("egypt.jpg")

