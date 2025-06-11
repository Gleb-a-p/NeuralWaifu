# config: utf-8

from fuzzywuzzy import fuzz
import vosk
import sys
import sounddevice as sd
import queue
import json

import app.modules.core.logic.config as config

# speech recognition model
model: vosk.Model = vosk.Model("model_small")
samplerate = 16000

q = queue.Queue()


def q_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


# Microphone listening function
def va_listen(callback, client, dialog, mod):
    with sd.RawInputStream(
            samplerate=samplerate,
            blocksize=8000,
            device=config.DEVICE,
            dtype="int16",
            channels=1,
            callback=q_callback
    ) as stream:
        rec = vosk.KaldiRecognizer(model, samplerate)
        music = ''

        while True:
            data = q.get()

            if rec.AcceptWaveform(data):
                # Suspend the microphone listening while the assistant is responding
                stream.stop()

                res = callback(
                    json.loads(rec.Result())["text"],
                    client,
                    dialog,
                    mod,
                    music
                )
                resp, music = res[0], res[1]

                # Resume listening to the microphone
                stream.start()


# Function for recognizing the assistant's name in a speech segment
def va_wake_word_recognition(word: str) -> bool:
    for name in config.VA_WAKE_WORD_LIST:
        detection_probability = fuzz.ratio(name, word)
        if detection_probability > config.NAME_PERCENT_DETECTION:
            print(f"Модель распознала свое имя с вероятностью {detection_probability}%")
            return True
    return False


# Function for trimming speech to a meaningful segment
def va_wake_word_detection(message: str) -> str:
    separated_message: list[str] = message.split()
    for i in range(len(separated_message)):
        if va_wake_word_recognition(separated_message[i]):
            ask = ''
            for word in separated_message[i + 1:]:
                ask += f"{word} "
            print(f"Модель распознала следующее обращение: {ask}")
            return ask
    return ''
