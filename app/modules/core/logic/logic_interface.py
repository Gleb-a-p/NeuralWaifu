# coding: utf-8
"""
This module includes a VA's logical module(core)
"""

import os
from fuzzywuzzy import fuzz
from g4f.client import Client
from openai import OpenAI
from pygame import mixer
import num2words
import random

from app.modules.core.state_interface import StateInterface # Changing VA state
from app.modules.windows.system_interface import SystemExecutor # Executing system commands


class Core:
    def __init__(
            self,
            id,
            name,
            system_name,
            version,
            operation_system,
            audio_detection_module,
            audio_synthesis_module,
            set_options_message,
            va_dialogue_history,
            va_llm_client,
            va_prompt,
            va_gpt_models,
            va_free_gpt_models,
            va_lmstudio_model,
            va_llm_modes,
            llm_client_checking_message,
            va_wws,
            va_speaking_cmds,
            va_void_cmds,
            base_browser,
            terraria_path,
            tmodloader_path,
            minecraft_path,
            goodbye_dpi_path,
            gallery_path,
            localhost_url,
            base_url,
            youtube_url,
            va_executed_answers,
            va_greeting,
            va_not_understand_answer,
            va_joker_list,
            va_praise_answers,
            va_censure_answers,
            va_calling_answers,
            va_potential_calling_answers,
            va_take_screenshot_answers,
            va_poweroff_messages,
            va_cmd_recognition_probability,
            va_base_volume,
            va_base_volume_up,
            va_base_volume_down,
            va_language,
            va_screenshot_name,
            va_screenshot_extension
    ) -> None:
        self.va_id = id
        self.va_name = name
        self.va_system_name = system_name
        self.va_version = version

        self.operation_system = operation_system

        self.set_options_message = set_options_message

        self.va_dialogue_history = va_dialogue_history
        self.va_llm_client = va_llm_client
        self.va_prompt = va_prompt
        self.llm_client_checking_message = llm_client_checking_message
        self.va_gpt_models = va_gpt_models
        self.va_free_gpt_models = va_free_gpt_models
        self.va_lmstudio_model = va_lmstudio_model
        self.va_llm_modes = va_llm_modes
        self.va_mod: str = self.set_mod("base") # choosing work mode for VA

        self.va_wws = va_wws

        self.va_speaking_cmds = va_speaking_cmds
        self.va_void_cmds = va_void_cmds

        self.base_browser = base_browser
        self.terraria_path = terraria_path
        self.tmodloader_path = tmodloader_path
        self.minecraft_path = minecraft_path
        self.goodbye_dpi_path = goodbye_dpi_path
        self.gallery_path = gallery_path

        self.localhost_url = localhost_url
        self.base_url = base_url
        self.youtube_url = youtube_url

        self.va_executed_answers = va_executed_answers
        self.va_greeting = va_greeting
        self.va_not_understand_answer = va_not_understand_answer
        self.va_joker_list = va_joker_list
        self.va_praise_answers = va_praise_answers
        self.va_censure_answers = va_censure_answers
        self.va_calling_answers = va_calling_answers
        self.va_potential_calling_answers = va_potential_calling_answers
        self.va_take_screenshot_answers = va_take_screenshot_answers
        self.va_poweroff_messages = va_poweroff_messages

        self.va_cmd_recognition_probability = va_cmd_recognition_probability
        self.va_base_volume = va_base_volume
        self.va_base_volume_up = va_base_volume_up
        self.va_base_volume_down = va_base_volume_down
        self.va_language = va_language
        self.va_screenshot_name = va_screenshot_name
        self.va_screenshot_extension = va_screenshot_extension
        self.va_music = '' # start value of music is not defined

        if self.va_mod == "free":
            self.va_llm_client=Client()
        elif self.va_mod == "lmstudio":
            self.va_llm_client=OpenAI(
                base_url=self.localhost_url,
                api_key="lm-studio"
            )

        self.adm = audio_detection_module
        self.asm = audio_synthesis_module
        self.state_interface: StateInterface = StateInterface()
        self.system_executor: SystemExecutor = SystemExecutor(
            self.va_system_name,
            self.operation_system,
            self.base_browser,
            self.gallery_path,
            self.va_language,
            self.va_screenshot_name,
            self.va_screenshot_extension
        )

    def __str__(self) -> str:
        return f"Core of {self.va_system_name} ({self.va_version}) with ID: {self.va_id}"

    # Getting debugging information
    def get_debug_info(self, api_key, time) -> None:
        print(
            f"{self.va_system_name} (v{self.va_version}) начал(а) свою работу ...\n"
            f"Имя: {self.va_name}\n"
            f"Api key: {api_key}\n"
            f"OpenAI client: {self.va_llm_client}\n"
            f"OS: {self.operation_system}\n"
            f"Mod = {self.va_mod}\n"
            f"Время на запуск: {time:.2f} секунд"
        )

    # Voice command reading function
    def va_respond(self, message) -> str:
        detected_message = self.adm.va_wake_word_detection(message)
        print(f"Detected message = {detected_message}")

        if detected_message:
            detected_message.strip()
            detected_message.strip('?')

        if detected_message != None:  # message.startswith(config.VA_WAKE_WORD_LIST):
            print(message)
            print(self.va_dialogue_history)

            print(f"К ассистенту обращаются с запросом [{detected_message}]")
            cmd = self.recognize_cmd(self.filter_cmd(message))
            print(cmd)

            response = ''

            if (
                    cmd["cmd"] not in self.va_speaking_cmds.keys() or
                    cmd["percent"] < self.va_cmd_recognition_probability
            ) and (
                    cmd["cmd"] not in self.va_void_cmds.keys() or
                    cmd["percent"] < self.va_cmd_recognition_probability
            ):
                try:
                    response = self.generate_response(
                        message=message,
                        mod=self.va_mod
                    )

                    corrected_response: str = self.correct_response(response)
                    print(corrected_response)

                    self.asm.va_speak(corrected_response)

                except Exception as err:
                    print(
                        f"Ошибка при получении ответа: {err}",
                        "Полный ответ смотрите в логах(dialogue_history, log.txt)"
                    )
            else:
                result = self.execute_cmd(
                    cmd['cmd'],
                )
                response = result

            separated_response = response.lstrip("<think>").split("</think>")
            thinks = "NONE"

            if len(separated_response) == 2:
                thinks, response = separated_response[0], separated_response[1]
            elif len(separated_response) == 1:
                response = separated_response[0]
            self.add_log(message, thinks, response)

            return response

        return ''

    # Voice command correction function
    def filter_cmd(self, raw_voice: str) -> str:
        cmd = raw_voice

        for word in self.va_wws:
            cmd = cmd.replace(word, '').strip()

        return cmd

    # Voice command recognition function
    def recognize_cmd(self, cmd: str) -> dict[str, str | int]:
        rc = {
            "cmd": '',
            "percent": 0
        }

        for command, variants in self.va_speaking_cmds.items():
            for word in variants:
                vrt = fuzz.ratio(cmd, word)

                if vrt > rc["percent"]:
                    rc["cmd"] = command
                    rc["percent"] = vrt

        for command, variants in self.va_void_cmds.items():
            for word in variants:
                vrt = fuzz.ratio(cmd, word)

                if vrt > rc["percent"]:
                    rc["cmd"] = command
                    rc["percent"] = vrt

        return rc

    # Voice command execution function
    def execute_cmd(self, cmd) -> str:
        text = self.va_not_understand_answer

        if cmd in self.va_speaking_cmds:
            match cmd:
                case "help":
                    text = self.va_greeting

                case "joke":
                    text = random.choice(self.va_joker_list)

                case "praise":
                    text = random.choice(self.va_praise_answers)

                case "censure":
                    text = random.choice(self.va_censure_answers)

                case "call":
                    text = random.choice(self.va_calling_answers)

                case "potential_call":
                    text = random.choice(self.va_potential_calling_answers)

        elif cmd in self.va_void_cmds:
            match cmd:
                case "current_time":
                    text: str = self.system_executor.get_current_time()

                case "open_browser":
                    self.system_executor.open_browser(self.base_url)
                    text: str = random.choice(self.va_executed_answers)

                case "open_youtube":
                    self.system_executor.open_browser(self.youtube_url)
                    text: str = random.choice(self.va_executed_answers)

                case "open_logs":
                    self.system_executor.open_text_file(
                        os.path.abspath("main.py")[:len(os.path.abspath("main.py")) - len("app/modules/core/logic/main.py")],
                        "log.txt"
                    )
                    text: str = random.choice(self.va_executed_answers)

                case "run_terraria":
                    self.system_executor.run_script(self.terraria_path)
                    text: str = random.choice(self.va_executed_answers)

                case "run_tmodloader":
                    self.system_executor.run_script(self.tmodloader_path)
                    text: str = random.choice(self.va_executed_answers)

                case "run_minecraft":
                    self.system_executor.run_script(self.minecraft_path)
                    text: str = random.choice(self.va_executed_answers)

                case "run_goodbye_dpi":
                    self.system_executor.run_script(self.goodbye_dpi_path)
                    text: str = random.choice(self.va_executed_answers)

                case "sleep":
                    self.state_interface.sleep()
                    text: str = random.choice(self.va_executed_answers)

                case "wake_up":
                    self.state_interface.wake_up(self.va_base_volume)
                    text: str = random.choice(self.va_executed_answers)

                case "max_volume":
                    self.state_interface.wake_up(1.0)
                    text: str = random.choice(self.va_executed_answers)

                case "volume_up":
                    self.state_interface.volume_up(self.va_base_volume_up)
                    text: str = random.choice(self.va_executed_answers)

                case "volume_down":
                    self.state_interface.volume_down(self.va_base_volume_down)
                    text: str = random.choice(self.va_executed_answers)

                case "turn_on_music":
                    text: str = random.choice(self.va_executed_answers)
                    self.asm.va_speak(text)
                    self.va_music: str = self.asm.turn_on_music()
                    print(f"Ответ от {self.va_name}: {text}")

                    return text

                case "stop_music":
                    mixer.music.pause()
                    text: str = random.choice(self.va_executed_answers)

                case "play_music":
                    text: str = random.choice(self.va_executed_answers)
                    self.asm.va_speak(text)
                    mixer.music.unpause()
                    print(f"Ответ от {self.va_name}: {text}")

                    return text

                case "change_music":
                    mixer.music.pause()
                    text: str = random.choice(self.va_executed_answers)
                    self.asm.va_speak(text)
                    self.va_music: str = self.asm.change_music(self.va_music)
                    print(f"Ответ от {self.va_name}: {text}")

                    return text

                case "loop_music":
                    mixer.music.play(-1)
                    text: str = random.choice(self.va_executed_answers)

                case "turn_off_music":
                    mixer.music.stop()
                    text: str = random.choice(self.va_executed_answers)

                case "take_screenshot":
                    self.system_executor.take_screenshot()
                    text: str = random.choice(self.va_executed_answers) + " . " + self.va_take_screenshot_answers

                case "get_geolocation":
                    current_location: tuple[str, str] = self.system_executor.get_location()
                    text: str = ("Текущее местоположение: "
                                 f"{current_location[0]} градусов по широте, "
                                 f"{current_location[1]} градусов по долготе.")

                case "get_battery_charge":
                    battery_charge: str = self.system_executor.get_battery_charge()
                    text: str = f"Текущий заряд батареи: {battery_charge} процентов."

                case "lock_computer":
                    text: str = random.choice(self.va_executed_answers)
                    self.asm.va_speak(text)
                    self.system_executor.run_script("rundll32 user32.dll, LockWorkStation")

                    return text

                case "computer_sleep":
                    text: str = random.choice(self.va_executed_answers)
                    self.asm.va_speak(text)
                    self.system_executor.run_script("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

                    return text

                case "poweroff":
                    self.poweroff()

        print(f"Ответ от {self.va_name}: {text}")
        self.asm.va_speak(text)

        return text

    # Response correction function
    def correct_response(self, response: str) -> str:
        bit_response = response.split()
        corrected_response = ''
        digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        flag = True

        for word in bit_response:
            for digit in digits:
                if digit in word:
                    corrected_response += f"{num2words.num2words(int(word), lang=self.va_language)} "
                    flag = False
                    break

            if flag: corrected_response += f"{word} "

            flag = True

        return corrected_response

    # Function for making request to LLM model
    def make_request(self, llm_client, model) -> str:
        try:
            chat_completion = llm_client.chat.completions.create(
                model=model,
                messages=self.va_dialogue_history,
                temperature = 0.6
            )

            response = chat_completion.choices[0].message.content.strip()

            self.va_dialogue_history.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )

            return response

        except Exception as err:
            print(err)

            return ''

    # Function for receiving a response from ChatGPT
    def generate_response(self, message: str, mod) -> str:
        try:
            # Adding instruction for communication style if it is new dialog
            if not self.va_dialogue_history:
                if mod == "base":
                    self.va_dialogue_history.append(
                        {
                            "role": "user",
                            "content": self.va_prompt
                        }
                    )
                    self.add_log(self.va_prompt, "NONE", "NONE", address="User")
                else:
                    self.va_dialogue_history.append(
                        {
                            "role": "system",
                            "content": self.va_prompt
                        }
                    )
                    self.add_log(self.va_prompt, "NONE", "NONE", address="System")

            self.va_dialogue_history.append(
                {
                    "role": "user",
                    "content": message
                }
            )

            # Getting a response from LLM Model
            match mod:
                case "base":  # If the API key for ChatGPT is working, use it
                    # Обращение к OpenAI API
                    # chat_completion = client.chat.completions.create(
                    #     model=config.GPT_MODEL,
                    #     messages=dialogue_history
                    # )

                    for model in self.va_gpt_models:  # Перебор возможных моделей
                        resp = self.make_request(self.va_llm_client, model)

                        if resp:
                            return resp

                case "free":  # Если апи-ключ для ChatGPT не рабочий, то используем свободную версию
                    for gpt_model in self.va_free_gpt_models:  # Перебор всевозможных free-моделей
                        resp = self.make_request(self.va_llm_client, gpt_model)

                        if resp:
                            return resp

                case "lmstudio":
                    return self.make_request(self.va_llm_client, self.va_lmstudio_model)

        except Exception as error:
            print(f"Произошла ошибка: {error}")
            print(f"Message: {message}")

            return ''

    # Function for obtaining a work mode for the assistant
    def get_mod(self) -> str:
        m = input(self.set_options_message)

        while m not in self.va_llm_modes.keys():
            m = input(self.set_options_message)
        else:
            mod: str = self.va_llm_modes[m]

        return mod

    # Function for correcting a work mode for the assistant
    def set_mod(self, mod) -> str:
        base_mod_response = self.generate_response(
                    self.llm_client_checking_message,
                    mod
                )

        # Checking the OpenAI client for correctness
        if not base_mod_response:  # If api key does not work, use free model
            free_mod_response = self.generate_response(
                        self.llm_client_checking_message,
                        "free"
                    )

            if not free_mod_response: # If free api does not work, use local model
                lmstudio_mod_response = self.generate_response(
                        self.llm_client_checking_message,
                        "lmstudio"
                    )

                self.add_log(
                    message=self.llm_client_checking_message,
                    thinks=lmstudio_mod_response.split("<think>")[0],
                    response=lmstudio_mod_response.split("<think>")[-1]
                )

                mod = "lmstudio"
            else:
                print("Base mode is not working. Please, choose one other mode.")

                self.add_log(message=self.llm_client_checking_message, thinks="NONE", response=free_mod_response)

                mod = self.get_mod()

                if mod == "base":
                    mod = "free"
        else:
            self.add_log(message=self.llm_client_checking_message, thinks="NONE", response=base_mod_response)

            mod = self.get_mod()

        print(self.va_dialogue_history)
        self.va_dialogue_history = []

        return mod

    # Function for adding logs to file
    def add_log(self, message, thinks, response, address="User") -> None:
        try:
            with open("../../../etc/log.txt", "a") as log:
                log.write(f"{address}: {message}\n")
                log.write(f"{self.va_name} thinks: {thinks}\n")
                log.write(f"{self.va_name}: {response}\n")
                log.write("\n")

        except Exception as err:
            print(f"Ошибка при прочтении лог-файла: {err}. Создается новый лог-файл.")

            try:
                with open(f"../../../etc/log{random.randint(1, 100)}.txt", "w") as log:
                    log.write(f"{address}: {message}\n")
                    log.write(f"{self.va_name} thinks: {thinks}\n")
                    log.write(f"{self.va_name}: {response}\n")
                    log.write("\n")

            except Exception as err:
                print(f"Не удалось создать новый лог-файл. Ошибка: {err}")

        log.close()

    # Function for turning off the assistant
    def poweroff(self) -> None:
        text: str = random.choice(self.va_poweroff_messages)
        self.asm.va_speak(text)
        print(f"Ответ от {self.va_name}: {text}")
        print(f"Завершение работы модели с ID: {self.va_id}")

        exit()
