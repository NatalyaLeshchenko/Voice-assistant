import vosk
import pyttsx3
import time
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('wordnet')
import json
import json

dialog_data = {
    "start": {
        "triggers": ["привет", "хелло"],
        "response": "Привет!",
        "yes": ["да"],
        "no": ["нет"],
        "yes_response": "Хорошо!",
        "no_response": "Окей, не важно."
    },
    "cola": {
        "triggers": ["кола", "колы", "колу"],
        "response": "Вы хотите выпить колы?",
        "yes": ["да"],
        "no": ["нет"],
        "yes_response": "Я знаю ближайший магазин",
        "True_shop" : ["магазин", "где"],
        "true_response": "Ближайший магазин через дорогу",
        "no_response": "Хм. А зачем спрашивали?"
    }
}

model = vosk.Model('D:/vosk/vosk_model')
rec = vosk.KaldiRecognizer(model, 16000)

lemmatizer = WordNetLemmatizer()

import pyaudio
import json

def listen_speech():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)
    print("Listening...")
    while True:
        data = stream.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = rec.Result()
            res_dict = json.loads(res)  
            if res_dict and "text" in res_dict:
                text = res_dict["text"]
                return text
    stream.stop_stream()
    stream.close()
    p.terminate()

def manipulate_text(text):
    return f"Вы сказали: {text}"

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

    
keyword_actions = {
    "песня": "Ла ла ла, ла ла ла, ла ла ла ла ла",
    "анекдот":"Почему книга по математике грустная? Потому что у нее много проблем",
    "дура": "Зачем вы обзываетесь? Мне обидно",
    ("робот", "вправо"): "Робот Маруся едет вправо",
    ("робот", "влево"): "Робот Маруся едет влево",
    ("робот", "вперед"): "Робот Маруся едет вперед",
    ("робот", "назад"): "Робот Маруся едет назад",
    ("сколько", "будет", "два","плюс", "два"): "Два плюс два будет четыре",
    ("уничтожить", "мир"): "Зачем вам уничтожать мир? Лучше посмотрите видео с котиками",
    ("поздравь", "с днём рождения"): "Поздравляю с днем рождения Желаю счастья от всего сердца",
    ("кола"): "Я знаю ближайший магазин с кока колой",
    
}    
    



def execute_voice_command(text, max_rec = 3, counter=0):
    print("Входной текст:", text)
    lemmas = [lemmatizer.lemmatize(token) for token in word_tokenize(text.lower())]
    print("Лемматизированный текст:", lemmas)
    
    for state, actions in dialog_data.items():
        if any(trigger in lemmas for trigger in actions['triggers']):
            trigger = next(trigger for trigger in actions['triggers'] if trigger in lemmas)
            print("Тригер-слово соответствует:", trigger)
            text_to_speech(actions['response'])
            response = listen_speech()
            
            if response:
                if any(word in response.lower() for word in actions['yes']):
                    text_to_speech(actions['yes_response'])
                elif any(word in response.lower() for word in actions['no']):
                    text_to_speech(actions['no_response'])
                elif any(word in response.lower() for word in actions['True_shop']):
                    text_to_speech(actions.get('true_response', ''))
                else:
                    handle_other_responses(response, state)
            if counter <max_rec:
                execute_voice_command(listen_speech())
            else: text_to_speech("Я утомилась, поговорим позже?")

def handle_other_responses(response, state):
    text_to_speech("Честно, вот, я ничего не поняла. Давайте еще раз")
    pass


wake_word = "маруся"
print("Assistant is listening for the wake word...")

while True:
    print("Listening for wake word...")
    text = listen_speech()
    if text and wake_word in text.lower():
        print("Wake word detected. What is your request?")
        text_to_speech("Привет!")
        time.sleep(0.5)
        command_text = listen_speech()
        if command_text:
            response_text = manipulate_text(command_text)
            execute_voice_command(command_text)