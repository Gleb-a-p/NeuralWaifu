# coding: utf-8

from fuzzywuzzy import fuzz
from g4f.client import Client
import num2words
import datetime
import webbrowser
import random
import os

import app.modules.core.logic.config as config
import app.modules.audio.audio_detection as a_d
import app.modules.audio.audio_speaking as a_s
import app.modules.core.changing_state.sleep as sleep
import app.modules.core.changing_state.wake_up as wake_up


# voice command reading function
def va_respond(message: str, client, dialogue_history, mod) -> None:
    print(message)
    detected_message = a_d.va_wake_word_detection(message)
    if detected_message:
        if message:
            print(message)
        print(f"К ассистенту обращаются с запросом [{detected_message}]")
        cmd = recognize_cmd(filter_cmd(message))
        print(cmd)
        if (
                cmd["cmd"] not in config.VA_SPEAKING_CMD_LIST.keys() or
                cmd["percent"] < config.CMD_PERCENT_DETECTION
        ) and (
                cmd["cmd"] not in config.VA_VOID_CMD_LIST.keys() or
                cmd["percent"] < config.CMD_PERCENT_DETECTION
        ):
            if mod == "base":
                try:
                    a_s.va_speak(generate_response(
                        dialogue_history,
                        message,
                        mod,
                        client
                    ))
                except Exception as err:
                    print(err)
            elif mod == "free":
                try:
                    a_s.va_speak(generate_response(
                        dialogue_history=dialogue_history,
                        message=message,
                        mod=mod
                    ))
                except Exception as err:
                    print(err)
        else:
            execute_cmd(cmd['cmd'])


# voice command correction function
def filter_cmd(raw_voice: str) -> str:
    cmd = raw_voice
    for word in config.VA_WAKE_WORD_LIST:
        cmd = cmd.replace(word, '').strip()
    for word in config.VA_TBR:
        cmd = cmd.replace(word, '').strip()
    return cmd


# voice command recognition function
def recognize_cmd(cmd: str) -> dict[str, str | int]:
    rc = {"cmd": '', "percent": 0}
    for command, variants in config.VA_SPEAKING_CMD_LIST.items():
        for word in variants:
            vrt = fuzz.ratio(cmd, word)
            if vrt > rc["percent"]:
                rc["cmd"] = command
                rc["percent"] = vrt
    for command, variants in config.VA_VOID_CMD_LIST.items():
        for word in variants:
            vrt = fuzz.ratio(cmd, word)
            if vrt > rc["percent"]:
                rc["cmd"] = command
                rc["percent"] = vrt
    return rc


# voice command execution function
def execute_cmd(cmd: str) -> None:
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
    elif cmd in config.VA_VOID_CMD_LIST:
        match cmd:
            case "current_time":
                now = datetime.datetime.now()
                text = f"Сейч+ас {num2words.num2words(
                    now.hour, lang=config.LANGUAGE
                )} {num2words.num2words(
                    now.minute, lang=config.LANGUAGE
                )}"
            case "open_browser":
                webbrowser.get(config.BASE_BROWSER).open_new_tab(config.BASE_URL)
                text = random.choice(config.EXECUTE_ANSWER)
            case "open_youtube":
                webbrowser.get(config.BASE_BROWSER).open_new_tab(config.YOUTUBE_URL)
                text = random.choice(config.EXECUTE_ANSWER)
            case "run_goodbye_dpi":
                os.system(config.GOODBYE_DPI_PATH)
                text = random.choice(config.EXECUTE_ANSWER)
            case "sleep":
                sleep.sleep()
                text = random.choice(config.EXECUTE_ANSWER)
            case "wake_up":
                wake_up.wake_up()
                text = random.choice(config.EXECUTE_ANSWER)
            case "turn_on_music":
                pass
            case "turn_off_music":
                pass
            case "poweroff":
                a_s.va_speak(random.choice(config.POWEROFF_MESSAGE_LIST))
                exit()
    print(f"Ответ от {config.VA_NAME}: {text}")
    a_s.va_speak(text)


# response correction function
def correct_response(response: str) -> str:
    bit_response = response.split()
    corrected_response = ''
    digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    flag = True
    for word in bit_response:
        for digit in digits:
            if digit in word:
                corrected_response += f"{num2words.num2words(
                    int(word), lang=config.LANGUAGE
                )} "
                flag = False
                break
        if flag: corrected_response += f"{word} "
        flag = True
    return corrected_response


# function for receiving a response from ChatGPT
def generate_response(dialogue_history: list[dict], message: str, mod: str, client=Client()):
    try:
        if not dialogue_history:
            dialogue_history.append(
                {"role": "system", "content": config.PROMPT}
            )
        dialogue_history.append(
            {"role": "user", "content": message}
        )
        if mod == "base":
            chat_completion = client.chat.completions.create(
                model=config.GPT_MODEL,
                messages=dialogue_history
            )
            response = chat_completion.choices[0].message.content.strip()
            dialogue_history.append(
                {"role": "assistant", "content": response}
            )
            corrected_response: str = correct_response(response)
            print(corrected_response)
            return corrected_response
        else:
            for gpt_model in config.GPT_MODEL_LIST:
                try:
                    chat_completion = client.chat.completions.create(
                        model=gpt_model,
                        messages=dialogue_history,
                    )
                    response = chat_completion.choices[0].message.content
                    dialogue_history.append(
                        {"role": "assistant", "content": response}
                    )
                    corrected_response: str = correct_response(response)
                    print(corrected_response)
                    return corrected_response
                except Exception as err:
                    print(err)
                    continue
            return None

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        print(f"Message: {message}")
        return None


# Function for obtaining a work mode for the assistant
def get_mod() -> str:
    mod: str = ''
    m = input(config.OPTIONS_MESSAGE)
    while m not in ('b', 'f'):
        m = input(config.OPTIONS_MESSAGE)
    else:
        if m == 'b':
            mod = "base"
        elif m == 'f':
            mod = "free"
    return mod
