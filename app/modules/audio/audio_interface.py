# config: utf-8
"""
This is a module sets VA's audio interface
"""

from fuzzywuzzy import fuzz
import vosk
import sys
import sounddevice as sd
import queue
import json

from random import choice
from pygame import mixer
import torch
import time
import os


class AudioDetection:
    def __init__(self, samplerate, device, wwd_list, name_percent_detection) -> None:
        self.model: vosk.Model = vosk.Model("model_small")

        self.samplerate = samplerate
        self.device = device
        self.wwd_list = wwd_list
        self.name_percent_detection = name_percent_detection

        self.q: queue.Queue = queue.Queue()

    def q_callback(self, indata, frames, time, status) -> None:
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    # Microphone listening function
    def va_listen(self, callback) -> None:
        with sd.RawInputStream(
                samplerate=self.samplerate,
                blocksize=8000,
                device=self.device,
                dtype="int16",
                channels=1,
                callback=self.q_callback
        ) as stream:
            rec = vosk.KaldiRecognizer(self.model, self.samplerate)

            while True:
                data = self.q.get()

                if rec.AcceptWaveform(data):
                    # Suspend the microphone listening while the assistant is responding
                    stream.stop()

                    res = callback(
                        json.loads(rec.Result())["text"],
                    )

                    # Resume listening to the microphone
                    stream.start()

    # Function for recognizing the assistant's name in a speech segment
    def va_wake_word_recognition(self, word: str) -> bool:
        for name in self.wwd_list:
            detection_probability = fuzz.ratio(name, word)

            if detection_probability > self.name_percent_detection:
                print(f"Модель распознала свое имя с вероятностью {detection_probability}%")

                return True

        return False

    # Function for trimming speech to a meaningful segment
    def va_wake_word_detection(self, message: str) -> str:
        separated_message: list[str] = message.split()

        for i in range(len(separated_message)):
            if self.va_wake_word_recognition(separated_message[i]):
                ask = ''

                for word in separated_message[i + 1:]:
                    ask += f"{word} "

                print(f"Модель распознала следующее обращение: {ask}")

                return ask

        return ''


class AudioSynthesis:
    def __init__(self, samplerate, relative_va_path, va_speaker) -> None:
        self.samplerate: int = samplerate
        self.relative_va_path: str = relative_va_path
        self.va_speaker = va_speaker

        self.device: torch.device = torch.device("cpu")  # cpu or gpu
        self.model, self._ = torch.hub.load(
            repo_or_dir="snakers4/silero-models",
            model="silero_tts",
            language="ru",
            speaker="ru_v3"
        )

        self.model.to(self.device)

    # Speech playback function
    def va_speak(self, message: str) -> None:
        audio = self.model.apply_tts(
            text=f"{message}..",
            speaker=self.va_speaker,  # aidar, baya, kseniya, xenia, random
            sample_rate=self.samplerate,
            put_accent=True,
            put_yo=True
        )
        sd.play(audio, self.samplerate * 1.05)
        time.sleep((len(audio) / self.samplerate) + 0.5)
        sd.stop()

    # Turning off music function
    def turn_on_music(self) -> str:
        music_path = os.path.abspath(self.relative_va_path).strip(
            self.relative_va_path) + "u/app" + "\modules\ ".strip() + "audio\music"
        music = music_path + f"/{choice(os.listdir(music_path))}"

        print("Доступная музыка: \n"
              f"{os.listdir(music_path)}")

        print(f"Текущая музыка: {music}")

        mixer.music.load(music)
        mixer.music.play()

        return music

    # Changing music function
    def change_music(self, old_music_path) -> str:
        music_path = os.path.abspath(self.relative_va_path).strip(
            self.relative_va_path) + "u/app" + "\modules\ ".strip() + "audio\music"

        old_music = old_music_path[len(music_path):]
        music = f"/{choice(os.listdir(music_path))}"

        if len(os.listdir(music_path)) > 1:
            while music == old_music:
                music = f"/{choice(os.listdir(music_path))}"

        print(f"Текущая музыка: {music}")

        mixer.music.load(music_path + music)
        mixer.music.play()
        print(
            f"Old music = {old_music}\n"
            f"New music = {music}"
        )

        return music_path + music
