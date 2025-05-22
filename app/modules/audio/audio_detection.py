# Импорт библиотек
import vosk
import sys
import sounddevice as sd
import queue
import json
from fuzzywuzzy import fuzz

# Импорт модулей
import app.modules.core.logic.config as config


model = vosk.Model("model_small") # ("model") # ("model_small") # модель, распознающая речь
samplerate = 16000

q = queue.Queue()


def q_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


# Функция прослушивания микрофона
def va_listen(callback, client, dialog, mod):
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=config.DEVICE, dtype='int16',
                           channels=1, callback=q_callback) as stream:
        rec = vosk.KaldiRecognizer(model, samplerate)

        while True:
            data = q.get()

            if rec.AcceptWaveform(data):
                stream.stop() # Приостанавливаем прослушивание микрофона на время ответа ассистента
                callback(json.loads(rec.Result())["text"], client, dialog, mod)
                stream.start() # Возобновляем прослушивание микрофона
            # else:
                # print(rec.PartialResult())


# Функция распознавания в отрезке речи имени ассистента
def va_wake_word_recognition(word):
    for name in config.VA_WAKE_WORD_LIST:
        detection_probability = fuzz.ratio(name, word)

        if detection_probability > config.NAME_PERCENT_DETECTION:
            print(f"Модель распознала свое имя с вероятностью {detection_probability}%")
            return True

    return False


# Функция обрезания речи до смыслового отрезка
def va_wake_word_detection(message):
    bit_message = message.split()

    for ind in range(len(bit_message)):
        if va_wake_word_recognition(bit_message[ind]):
            ask = ""

            for word in bit_message[ind + 1:]:
                ask += word + " "

            print(f"Модель распознала распознала следующее обращение: {ask}")
            return ask

    return False
    # return message.startswith(config.VA_WAKE_WORD_LIST)
