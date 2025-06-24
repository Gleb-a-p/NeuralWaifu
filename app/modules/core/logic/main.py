# -*-coding: utf-8 -*-
"""
This is main file with import
of all necessary libraries and functions.
You need run this file to run project.
"""

from openai import OpenAI
from PyQt6.QtWidgets import QApplication
from pygame import mixer
import random
import configparser
import webbrowser
import time
import sys

import app.modules.core.logic.config as config # Configuration
import app.modules.graphics.gui as gui # Graphical interface
from app.modules.audio.audio_interface import AudioDetection, AudioSynthesis # Audio
# import app.modules.core.logic.dialogue as dialogue # Dialogue logic(Chat GPT)
# import app.modules.audio.audio_detection as audio_detection # Audio(recognition)
# import app.modules.audio.audio_speaking as audio_speaking # Audio(synthesis)
from app.modules.core.logic.logic_interface import Core # Core of VA


class VoiceAssistance:
    def __init__(
            self,
            id,
            name,
            version,
            set_options_message,
            api_key,
            va_dialogue_history,
            base_gpt_url,
            va_prompt,
            va_gpt_models,
            va_free_gpt_models,
            llm_client_checking_message,
            va_wws,
            va_speaking_cmds,
            va_void_cmds,
            base_browser,
            terraria_path,
            tmodloader_path,
            base_browser_path,
            goodbye_dpi_path,
            gallery_path,
            base_url,
            youtube_url,
            va_greetings,
            va_executed_answers,
            va_greeting_message,
            va_not_understand_answer,
            va_joker_list,
            va_praise_answers,
            va_censure_answers,
            va_calling_answers,
            va_take_screenshot_answers,
            va_poweroff_messages,
            va_cmd_recognition_probability,
            va_base_volume,
            va_base_volume_up,
            va_base_volume_down,
            va_language,
            va_screenshot_name,
            va_screenshot_extension,
            detecting_samplerate,
            synthesis_samplerate,
            va_device,
            va_relative_path
    ) -> None:
        self.start: float = time.time()  # recording the program launch time

        self.va_id = id
        self.va_name = name
        self.va_version = version

        # self.uim = gui_module
        # self.adm = audio_detection_module
        # self.asm = audio_synthesis_module

        self.set_options_message = set_options_message

        self.api_key = api_key
        self.va_dialogue_history = va_dialogue_history
        self.base_gpt_url = base_gpt_url
        # Initializing an OpenAI client
        self.va_llm_client: OpenAI = OpenAI(
            api_key=self.api_key,
            base_url=config.BASE_GPT_URL # base_url="https://api.proxyapi.ru/openai/v1",
        )
        self.va_prompt = va_prompt
        self.llm_client_checking_message = llm_client_checking_message
        self.va_gpt_models = va_gpt_models
        self.va_free_gpt_models = va_free_gpt_models

        self.va_wws = va_wws

        self.va_speaking_cmds = va_speaking_cmds
        self.va_void_cmds = va_void_cmds

        self.base_browser = base_browser
        self.terraria_path = terraria_path
        self.tmodloader_path = tmodloader_path
        self.base_browser_path = base_browser_path
        self.goodbye_dpi_path = goodbye_dpi_path
        self.gallery_path = gallery_path

        self.base_url = base_url
        self.youtube_url = youtube_url

        self.va_greetings = va_greetings
        self.va_executed_answers = va_executed_answers
        self.va_greeting_message = va_greeting_message
        self.va_not_understand_answer = va_not_understand_answer
        self.va_joker_list = va_joker_list
        self.va_praise_answers = va_praise_answers
        self.va_censure_answers = va_censure_answers
        self.va_calling_answers = va_calling_answers
        self.va_take_screenshot_answers = va_take_screenshot_answers
        self.va_poweroff_messages = va_poweroff_messages

        self.va_cmd_recognition_probability = va_cmd_recognition_probability
        self.va_base_volume = va_base_volume
        self.va_base_volume_up = va_base_volume_up
        self.va_base_volume_down = va_base_volume_down
        self.va_language = va_language
        self.va_screenshot_name = va_screenshot_name
        self.va_screenshot_extension = va_screenshot_extension

        self.detecting_samplerate = detecting_samplerate
        self.synthesis_samplerate = synthesis_samplerate
        self.va_device = va_device
        self.va_relative_path = va_relative_path

        # Creating an application
        self.app: QApplication = QApplication(sys.argv)

        self.audio_detect_module = AudioDetection(
            self.detecting_samplerate,
            self.va_device,
            self.va_wws,
            self.va_cmd_recognition_probability
        )

        self.audio_synthes_module = AudioSynthesis(
            self.synthesis_samplerate,
            self.va_relative_path
        )

        # Creating core of VA
        self.NeuralWaifu = Core(
            self.va_id,
            self.va_name,
            self.va_version,
            self.audio_detect_module,
            self.audio_synthes_module,
            self.set_options_message,
            self.va_dialogue_history,
            self.va_llm_client,
            self.va_prompt,
            self.va_gpt_models,
            self.va_free_gpt_models,
            self.llm_client_checking_message,
            self.va_wws,
            self.va_speaking_cmds,
            self.va_void_cmds,
            self.base_browser,
            self.terraria_path,
            self.tmodloader_path,
            self.goodbye_dpi_path,
            self.gallery_path,
            self.base_url,
            self.youtube_url,
            self.va_executed_answers,
            self.va_greeting_message,
            self.va_not_understand_answer,
            self.va_joker_list,
            self.va_praise_answers,
            self.va_censure_answers,
            self.va_calling_answers,
            self.va_take_screenshot_answers,
            self.va_poweroff_messages,
            self.va_cmd_recognition_probability,
            self.va_base_volume,
            self.va_base_volume_up,
            self.va_base_volume_down,
            self.va_language,
            self.va_screenshot_name,
            self.va_screenshot_extension
        )

        # Creating MainWindow
        self.window: gui.MainWindow = gui.MainWindow(self.NeuralWaifu, self.va_name)

        # Fix the browser path
        webbrowser.register(
            self.base_browser,
            None,
            webbrowser.BackgroundBrowser(self.base_browser_path)
        )

        mixer.init()  # Initializing music mixer

        self.end: float = time.time() # recording the end time of the program launch

    def __str__(self) -> str:
        return f"Voice Assistant {self.va_name} ({self.va_version}) with ID:{self.va_id}"

    def run(self) -> None:
        self.window.show()

        # Output debugging information
        print(self.NeuralWaifu)
        self.NeuralWaifu.get_debug_info( self.api_key, round(self.end - self.start, 1) )

        # Starting the event loop
        self.app.exec()

        # Starting the voice assistant
        self.audio_synthes_module.va_speak(
            random.choice(self.va_greetings)
        )  # greeting at startup
        self.audio_detect_module.va_listen(
            self.NeuralWaifu.va_respond,
        )  # start listening to commands


def main():
    # Reading data from the configuration file
    conf: configparser.ConfigParser = configparser.ConfigParser()
    conf.read("../../../etc/config.ini")
    api_key: str = conf['DEFAULT']['Api_key']

    dialogue_history: list = [] # list for storing dialog history

    Jarvis: VoiceAssistance = VoiceAssistance(
        config.VA_ROOT_ID,
        config.VA_NAME,
        config.VA_VERSION,
        config.OPTIONS_MESSAGE,
        api_key,
        dialogue_history,
        config.BASE_GPT_URL,
        config.PROMPT,
        config.GPT_MODEL_LIST,
        config.GPT_FREE_MODEL_LIST,
        config.CHECKING_MESSAGE,
        config.VA_WAKE_WORD_LIST,
        config.VA_SPEAKING_CMD_LIST,
        config.VA_VOID_CMD_LIST,
        config.BASE_BROWSER,
        config.TERRARIA_PATH,
        config.TMODLOADER_PATH,
        config.CHROME_PATH,
        config.GOODBYE_DPI_PATH,
        config.GALLERY_PATH,
        config.BASE_URL,
        config.YOUTUBE_URL,
        config.GREETING_LIST,
        config.EXECUTED_ANSWER_LIST,
        config.GREETING_MESSAGE,
        config.NOT_UNDERSTAND_ANSWER,
        config.JOKER_LIST,
        config.PRAISE_ANSWERS,
        config.CENSURE_ANSWERS,
        config.CALL_ANSWERS,
        config.TAKE_SCREENSHOT_ANSWER,
        config.POWEROFF_MESSAGE_LIST,
        config.CMD_PERCENT_DETECTION,
        config.BASE_VOLUME,
        config.BASE_VOLUME_UP,
        config.BASE_VOLUME_DOWN,
        config.VA_LANGUAGE,
        config.SCREENSHOT_NAME,
        config.SCREENSHOT_EXTENSION,
        config.DETECTING_SAMPLERATE,
        config.SYNTHESIS_SAMPLERATE,
        config.DEVICE,
        config.RELATIVE_VA_PATH
    )

    print(Jarvis)
    Jarvis.run()


if __name__ == "__main__":
    main()
