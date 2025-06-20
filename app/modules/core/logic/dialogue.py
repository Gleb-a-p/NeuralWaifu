# coding: utf-8

from fuzzywuzzy import fuzz
from g4f.client import Client
from pygame import mixer
import num2words
import random

import app.modules.core.logic.config as config # Configuration
import app.modules.audio.audio_detection as audio_detection # Audio(detection)
import app.modules.audio.audio_speaking as audio_speaking # Audio(synthesis)
from app.modules.core.state_interface import StateInterface # Changing VA state
from app.modules.windows.system_actions import SystemExecutor # Executing system commands


# Voice command reading function
def va_respond(message, client, dialogue_history, mod, music) -> tuple[str, str]:
    detected_message = (audio_detection.va_wake_word_detection(message))
    print(f"Detected message = {detected_message}")

    if detected_message:
        detected_message.strip()
        detected_message.strip('?')

    if detected_message: # message.startswith(config.VA_WAKE_WORD_LIST):
        print(message)

        print(f"К ассистенту обращаются с запросом [{detected_message}]")
        cmd = recognize_cmd(filter_cmd(message))
        print(cmd)

        response = ''

        if (
                cmd["cmd"] not in config.VA_SPEAKING_CMD_LIST.keys() or
                cmd["percent"] <= config.CMD_PERCENT_DETECTION
        ) and (
                cmd["cmd"] not in config.VA_VOID_CMD_LIST.keys() or
                cmd["percent"] <= config.CMD_PERCENT_DETECTION
        ):
            match mod:
                case "base":
                    try:
                        response = generate_response(
                            dialogue_history,
                            message,
                            mod,
                            client
                        )
                        audio_speaking.va_speak(response)

                    except Exception as err:
                        print(
                            f"Ошибка при получении ответа: {err}",
                            "Полный ответ смотрите в логах(dialogue_history)"
                        )
                case "free":
                    try:
                        response = generate_response(
                            dialogue_history=dialogue_history,
                            message=message,
                            mod=mod
                        )
                        audio_speaking.va_speak(response)

                    except Exception as err:
                        print(
                            f"Ошибка при получении ответа: {err}",
                            "Полный ответ смотрите в логах(dialogue_history)"
                        )
        else:
            result = execute_cmd(
                cmd['cmd'],
                music
            )
            response, music = result[0], result[1]

        return response, music

    return '', music


# Voice command correction function
def filter_cmd(raw_voice: str) -> str:
    cmd = raw_voice

    for word in config.VA_WAKE_WORD_LIST:
        cmd = cmd.replace(word, '').strip()

    return cmd


# Voice command recognition function
def recognize_cmd(cmd: str) -> dict[str, str | int]:
    rc = {"cmd": '', "percent": 0}

    for command, variants in config.VA_SPEAKING_CMD_LIST.items():
        for word in variants:
            vrt = fuzz.ratio(cmd, word)

            if vrt > rc['percent']:
                rc['cmd'] = command
                rc['percent'] = vrt

    for command, variants in config.VA_VOID_CMD_LIST.items():
        for word in variants:
            vrt = fuzz.ratio(cmd, word)

            if vrt > rc['percent']:
                rc['cmd'] = command
                rc['percent'] = vrt

    return rc


# Voice command execution function
def execute_cmd(cmd, music) -> tuple[str, str]:
    state_interface: StateInterface = StateInterface()
    system_executor: SystemExecutor = SystemExecutor(
        config.BASE_BROWSER,
        config.GALLERY_PATH,
        config.LANGUAGE,
        config.SCREENSHOT_NAME,
        config.SCREENSHOT_EXTENSION
    )

    text = config.NOT_UNDERSTAND_ANSWER

    if cmd in config.VA_SPEAKING_CMD_LIST:
        match cmd:
            case "help":
                text = config.GREETING_MESSAGE

            case "joke":
                text = random.choice(config.JOKER_LIST)

            case "praise":
                text = random.choice(config.PRAISE_ANSWER)

            case "censure":
                text = random.choice(config.CENSURE_ANSWER)

            case 'call':
                text = random.choice(config.CALL_ANSWER)

    elif cmd in config.VA_VOID_CMD_LIST:
        match cmd:
            case "current_time":
                text: str = system_executor.get_current_time()

            case "open_browser":
                system_executor.open_browser(config.BASE_URL)
                text: str = random.choice(config.EXECUTE_ANSWER)

            case "open_youtube":
                system_executor.open_browser(config.YOUTUBE_URL)
                text: str = random.choice(config.EXECUTE_ANSWER)

            case "run_terraria":
                system_executor.run_script(config.TERRARIA_PATH)
                text: str = random.choice(config.EXECUTE_ANSWER)

            case "run_tmodloader":
                system_executor.run_script(config.TMODLOADER_PATH)
                text: str = random.choice(config.EXECUTE_ANSWER)

            case "run_goodbye_dpi":
                system_executor.run_script(config.GOODBYE_DPI_PATH)
                text: str = random.choice(config.EXECUTE_ANSWER)

            case "sleep":
                state_interface.sleep()
                text: str = random.choice(config.EXECUTE_ANSWER)

            case "wake_up":
                state_interface.wake_up(config.BASE_VOLUME)
                text: str = random.choice(config.EXECUTE_ANSWER)

            case "max_volume":
                state_interface.wake_up(1.0)
                text: str = random.choice(config.EXECUTE_ANSWER)

            case "volume_up":
                state_interface.volume_up(config.BASE_VOLUME_UP)
                text: str = random.choice(config.EXECUTE_ANSWER)

            case "volume_down":
                state_interface.volume_down(config.BASE_VOLUME_DOWN)
                text: str = random.choice(config.EXECUTE_ANSWER)

            case "turn_on_music":
                text: str = random.choice(config.EXECUTE_ANSWER)
                audio_speaking.va_speak(text)
                music: str = audio_speaking.turn_on_music()
                print(f"Ответ от {config.VA_NAME}: {text}")
                return text, music

            case "stop_music":
                mixer.music.pause()
                text: str = random.choice(config.EXECUTE_ANSWER)

            case "play_music":
                text: str = random.choice(config.EXECUTE_ANSWER)
                audio_speaking.va_speak(text)
                mixer.music.unpause()
                print(f"Ответ от {config.VA_NAME}: {text}")
                return text, music

            case "change_music":
                mixer.music.pause()
                text: str = random.choice(config.EXECUTE_ANSWER)
                audio_speaking.va_speak(text)
                music: str = audio_speaking.change_music(music)
                print(f"Ответ от {config.VA_NAME}: {text}")
                return text, music

            case "turn_off_music":
                mixer.music.stop()
                text: str = random.choice(config.EXECUTE_ANSWER)

            case "take_screenshot":
                system_executor.take_screenshot()
                text: str = random.choice(config.EXECUTE_ANSWER) + " . " + config.TAKE_SCREENSHOT_ANSWER

            case "get_geolocation":
                current_location: tuple[str, str] = system_executor.get_location()
                text: str = ("Текущее местоположение: "
                             f"{current_location[0]} градусов по широте, "
                             f"{current_location[1]} градусов по долготе.")

            case "poweroff":
                text: str = random.choice(config.POWEROFF_MESSAGE_LIST)
                audio_speaking.va_speak(text)
                print(f"Ответ от {config.VA_NAME}: {text}")
                exit()

    print(f"Ответ от {config.VA_NAME}: {text}")
    audio_speaking.va_speak(text)

    return text, music


# Response correction function
def correct_response(response: str) -> str:
    bit_response = response.split()
    corrected_response = ''
    digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    flag = True

    for word in bit_response:
        for digit in digits:
            if digit in word:
                corrected_response += f"{num2words.num2words(int(word), lang=config.LANGUAGE)} "
                flag = False
                break

        if flag: corrected_response += f"{word} "

        flag = True

    return corrected_response


# Function for receiving a response from ChatGPT
def generate_response(dialogue_history: list[dict], message: str, mod: str, client=Client()) -> str:
    try:
        # Adding instruction for communication style if it is new dialog
        if not dialogue_history:
            dialogue_history.append(
                {
                    "role": "user",
                    "content": config.PROMPT
                }
            )

        dialogue_history.append(
            {
                "role": "user",
                "content": message
            }
        )

        # G
        if mod == "base": # If the API key for ChatGPT is working, use it
            # Обращение к OpenAI API
            # chat_completion = client.chat.completions.create(
            #     model=config.GPT_MODEL,
            #     messages=dialogue_history
            # )

            for model in config.GPT_MODEL_LIST: # Перебор возможных моделей
                try:
                    chat_completion = client.chat.completions.create(
                        model = model,
                        messages = dialogue_history
                    )

                    response = chat_completion.choices[0].message.content.strip()

                    dialogue_history.append(
                        {
                            "role": "assistant",
                            "content": response
                        }
                    )

                    corrected_response: str = correct_response(response)
                    print(corrected_response)

                    return corrected_response

                except Exception as err:
                    print(err)
                    continue

        elif mod == "free":  # Если апи-ключ для ChatGPT не рабочий, то используем свободную версию
            for gpt_model in config.GPT_FREE_MODEL_LIST: # Перебор всевозможных free-моделей
                try:
                    chat_completion = client.chat.completions.create(
                        model=gpt_model,
                        messages=dialogue_history,
                    )
                    response = chat_completion.choices[0].message.content

                    dialogue_history.append(
                        {
                            "role": "assistant",
                            "content": response
                        }
                    )

                    corrected_response: str = correct_response(response)
                    print(corrected_response)

                    return corrected_response

                except Exception as err:
                    print(err)
                    continue

    except Exception as error:
        print(f"Произошла ошибка: {error}")
        print(f"Message: {message}")

        return ''


# Function for obtaining a work mode for the assistant
def get_mod() -> str:
    mod: str = ''
    m = input(config.OPTIONS_MESSAGE)

    while m not in ('b', 'f'):
        m = input(config.OPTIONS_MESSAGE)
    else:
        match m:
            case 'b':
                mod = "base"

            case 'f':
                mod = "free"

    return mod
