# coding: utf-8

from random import choice
from pygame import mixer
import sounddevice
import torch
import time
import os

import app.modules.core.logic.config as config


sample_rate: int = 48000
device: torch.device = torch.device("cpu")  # cpu or gpu
model, _ = torch.hub.load(
    repo_or_dir="snakers4/silero-models",
    model="silero_tts",
    language="ru",
    speaker="ru_v3"
)
model.to(device)


# Speech playback function
def va_speak(what: str) -> None:
    audio = model.apply_tts(
        text=f"{what}..",
        speaker="aidar",  # aidar, baya, kseniya, xenia, random
        sample_rate=sample_rate,
        put_accent=True,
        put_yo=True
    )
    sounddevice.play(audio, sample_rate * 1.05)
    time.sleep((len(audio) / sample_rate) + 0.5)
    sounddevice.stop()


# Turning off music function
def turn_on_music() -> str:
    music_path = os.path.abspath(config.RELATIVE_VA_PATH).strip(config.RELATIVE_VA_PATH) + "u/app" + "\modules\ ".strip() + "audio\music"
    music = music_path + f"/{choice(os.listdir(music_path))}"

    mixer.music.load(music)
    mixer.music.play()

    return music


# Changing music function
def change_music(old_music_path) -> str:
    music_path = os.path.abspath(config.RELATIVE_VA_PATH).strip(config.RELATIVE_VA_PATH) + "u/app" + "\modules\ ".strip() + "audio\music"

    old_music = old_music_path[len(music_path):]
    music = f"/{choice(os.listdir(music_path))}"

    if len(os.listdir(music_path)) > 1:
        while music == old_music:
            music = f"/{choice(os.listdir(music_path))}"

    mixer.music.load(music_path + music)
    mixer.music.play()
    print(
        f"Old music = {old_music}\n"
        f"New music = {music}"
    )

    return music_path + music