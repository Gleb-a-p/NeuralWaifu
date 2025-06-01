# Импорт библиотек
from fuzzywuzzy import fuzz
from num2t4ru import num2text
from g4f.client import Client
import datetime
import webbrowser
import random
import os

# Импорт модулей
import app.modules.core.logic.config as config # Модуль конфигурации
import app.modules.audio.audio_detection as audio_detection # Модуль работы с речью(распознавание)
import app.modules.audio.audio_speaking as audio_speaking # Модуль работы с речью(синтез)
import app.modules.core.changing_state.sleep as sleep # Модуль засыпания
import app.modules.core.changing_state.wake_up as wake_up # Модуль пробуждения


# Функция считывания голосовой команды
def va_respond(message: str, client, dialogue_history, mod):
    detected_message = (audio_detection.va_wake_word_detection(message))
    print(f"Detected message = {detected_message}")
    if detected_message:
        detected_message.strip('?') # Распознаем сообщение

    if detected_message: # message.startswith(config.VA_WAKE_WORD_LIST):
        print(message)

        # Обращаются к ассистенту
        print(f"К ассистенту обращаются с запросом [{detected_message}]")
        cmd = recognize_cmd(filter_cmd(message)) # Получение распознанной команды
        print(cmd)

        if ( ( cmd['cmd'] not in config.VA_SPEAKING_CMD_LIST.keys() or cmd['percent'] < config.CMD_PERCENT_DETECTION ) and ( cmd['cmd'] not in config.VA_VOID_CMD_LIST.keys() or cmd['percent'] < config.CMD_PERCENT_DETECTION ) ): # or ( cmd == 'usual_answer' ):
            if mod == "base":
                try:
                    response = generate_response(dialogue_history, message, mod, client)
                    audio_speaking.va_speak(response)
                except Exception as err:
                    print(err)
            elif mod == "free":
                try:
                    response = generate_response(dialogue_history=dialogue_history, message=message, mod=mod)
                    audio_speaking.va_speak(response)
                except Exception as err:
                    print(
                        f"Ошибка при получении ответа: {err}",
                        "Полный ответ смотрите в логах(dialogue_history)"
                    )
        else:
            response = execute_cmd(cmd['cmd'])

        return response


# Функция корректировки голосовой команды
def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for word in config.VA_WAKE_WORD_LIST:
        cmd = cmd.replace(word, "").strip()

    for word in config.VA_TBR:
        cmd = cmd.replace(word, "").strip()

    return cmd


# Функция распознавания голосовой команды
def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}

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


# Функция исполнения голосовой команды
def execute_cmd(cmd: str):
    text = config.NOT_UNDERSTAND_ANSWER

    if cmd in config.VA_SPEAKING_CMD_LIST:
        if cmd == 'help': # get help
            text = config.GREETING_MESSAGE

        elif cmd == 'joke': # get joke
            text = random.choice(config.JOKER_LIST)

        elif cmd == 'praise': # reaction for praise
            text = random.choice(config.PRAISE_ANSWER)

        elif cmd == 'censure': # reaction for censure
            text = random.choice(config.CENSURE_ANSWER)

        elif cmd == 'call':
            text = random.choice(config.CALL_ANSWER)

    elif cmd in config.VA_VOID_CMD_LIST:
        if cmd == 'current_time': # get current time
            now = datetime.datetime.now()
            text = "Сейчас " + num2text(now.hour) + " " + num2text(now.minute)

        elif cmd == 'open_browser': # open browser
            # chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
            # webbrowser.get(chrome_path).open("http://python.org")
            webbrowser.get(config.BASE_BROWSER).open_new_tab(config.BASE_URL)
            # webbrowser.open_new_tab(config.BASE_URL, new=1) # get(using=config.BASE_BROWSER).open_new_tab(config.BASE_URL)
            text = random.choice(config.EXECUTE_ANSWER) # Сообщаем о выполнении команды

        elif cmd == 'open_youtube': # open youtube
            webbrowser.get(config.BASE_BROWSER).open_new_tab(config.YOUTUBE_URL)
            text = random.choice(config.EXECUTE_ANSWER)  # Сообщаем о выполнении команды

        elif cmd == 'run_goodbye_dpi': # run Goodbye DPI
            os.system(config.GOODBYE_DPI_PATH)
            text = random.choice(config.EXECUTE_ANSWER)  # Сообщаем о выполнении команды

        elif cmd == 'sleep': # set volume to minimal value
            text = random.choice(config.EXECUTE_ANSWER)  # Сообщаем о выполнении команды
            # os.system("powershell.exe (Get-WmiObject -Class 'win32_volumecontrol').SetVolume(0)")

            sleep.sleep() # Засыпание

        elif cmd == 'wake_up': # set volume to normal value
            # os.system("powershell.exe (Get-WmiObject -Class 'win32_volumecontrol').SetVolume(60)")
            wake_up.wake_up() # Пробуждение

            text = random.choice(config.EXECUTE_ANSWER)  # Сообщаем о выполнении команды

        elif cmd == 'turn_on_music': # turn on random music
            pass
            # text = random.choice(config.EXECUTE_ANSWER)  # Сообщаем о выполнении команды

        elif cmd == 'turn_off_music': # turn off playing music
            pass
            # text = random.choice(config.EXECUTE_ANSWER)  # Сообщаем о выполнении команды

        elif cmd == 'poweroff': # shut down
            audio_speaking.va_speak(random.choice(config.POWEROFF_MESSAGE_LIST))
            exit()

    print(f"Ответ от {config.VA_NAME}: {text}") # Вывод ответа ассистента в консоль
    audio_speaking.va_speak(text) # Сообщение ответа
    return text


# Функция корректировки ответа
def correct_response(response):
    bit_response = response.split()
    corrected_response = ""
    digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

    flag = True
    for word in bit_response:
        for digit in digits:
            if digit in word:
                corrected_response += str(num2text(int(word))) + " "
                flag = False
                break

        if flag:
            corrected_response += word + " "

        flag = True

    return corrected_response


# Функция получения ответа от ChatGPT
def generate_response(dialogue_history, message, mod, client=Client()): # Получение ответа от ИИ(ChatGPT 3.5 turbo 1106)
    try:
        # Если это новый диалог, добавляем инструкцию для стиля общения
        if not dialogue_history:
            dialogue_history.append(
                {
                    "role": "user",
                    "content": config.PROMPT
                }
            )

        # Добавление текущего сообщения в историю
        dialogue_history.append(
            {
                "role": "user",
                "content": message
            }
        )

        if mod == "base": # Если апи-ключ для ChatGPT рабочий, то используем его
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

                    dialogue_history.append({"role": "assistant", "content": response})

                    corrected_response = correct_response(response)
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

                    dialogue_history.append({"role": "assistant", "content": response})

                    corrected_response = correct_response(response)
                    print(corrected_response)

                    return corrected_response

                except Exception as err:
                    print(err)
                    continue

    except Exception as error:
        print(f"Произошла ошибка: {str(error)}")
        print(f"Message: {message}")


# Функция получения режима работы ассистента
def get_mod():
    m = input(config.OPTIONS_MESSAGE)

    while not (m in ['b', 'f']):
        m = input(config.OPTIONS_MESSAGE)

    else:
        if m == 'b':
            mod = "base"
        elif m == 'f':
            mod = "free"

    return mod
