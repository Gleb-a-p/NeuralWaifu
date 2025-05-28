# coding: utf-8

import sounddevice
import torch
import time

sample_rate: int = 48000
device: torch.device = torch.device("cpu")  # cpu or gpu
model, _ = torch.hub.load(
    repo_or_dir="snakers4/silero-models",
    model="silero_tts",
    language="ru",
    speaker="ru_v3"
)
model.to(device)


# speech playback function
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
