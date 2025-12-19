# coding: utf-8
"""
This is a configuration module with general VA settings
"""

# import os
import platform


# Voice assistant
VA_VERSION: str = "1.2.6b"

VA_MODES: list[list[str]] = [
    ["j", "Jarvis"],
    ["m", "Mita"],
    # ["w", "Wendy"],
    ["j", "m"]
]

# Command recognition word lists
VA_SPEAKING_CMD_LIST: dict[str: list[str]] = {
    # "usual_answer": [
    #     "объясни",
    #     "почему",
    #     "кто такой"
    # ],
    "help": [
        "список команд",
        "кто ты",
        "ты кто",
        "команды",
        "что ты умеешь",
        "твои навыки",
        "навыки",
        "умения",
        "расскажи о себе"
    ],
    "joke": [
        "расскажи анекдот",
        "рассмеши",
        "шутка",
        "расскажи шутку",
        "пошути",
        "развесели",
        "расскажи тупую шутку"
    ],
    "praise": [
        "ты молодец",
        "молодец",
        "ты красава",
        "красава",
        "ты красавчик",
        "красавчик",
        "ты лучший",
        "спасибо"
    ],
    "censure": [
        "ты дурак",
        "ты бесполезный",
        "ты баран",
        "ты идиот",
        "ты тупой"
    ],
    "call": [
        "ты тут",
        # ''
    ],
    "potential_call": [
        ' ',
        ''
    ]
}

VA_VOID_CMD_LIST: dict[str: list[str]] = {
    "current_time": [
        "время",
        "текущее время",
        "сейчас времени",
        "который час",
        "сколько время"
    ],
    "open_browser": [
        "открой браузер",
        "запусти браузер",
        "открой гугл хром",
        "гугл хром",
        "хром",
        "гугл",
        "открой гугл",
        "открой хром"
    ],
    "open_youtube": [
        "открой ютуб",
        "ютуб",
        "запусти ютуб"
    ],
    "open_logs": [
        "открой историю диалога",
        "открой лог файл",
        "открой логи",
        "покажи логи",
        "логи"
    ],
    "run_terraria": [
        "запусти террарию",
        "запусти терку",
        "запусти террария",
        "запусти терру"
    ],
    "run_tmodloader": [
        "запусти модовую террарию",
        "запусти террарию с модами",
        "запусти т мод лоадер",
        "запусти мод лоадер"
    ],
    "run_minecraft": [
        "майнкрафт",
        "запусти майнкрафт",
        "запусти майн",
        "открой майнкрафт",
        "минекрафт"
    ],
    "run_tlauncher": [
        "пиратский майнкрафт",
        "запусти пиратский майнкрафт",
        "пиратский минекрафт",
        "т лаунчер",
        "запусти т лаунчер",
    ],
    "run_goodbye_dpi": [
        "запусти гудбай д п ай",
        "запусти гудбай",
        "гудбай д п ай",
        "запусти обход блокировок"
    ],
    "sleep": [
        "не мешай",
        "без звука",
        "выключи звук",
        "спи",
        "спать",
        "убери звук"
    ],
    "wake_up": [
        "вставай",
        "со звуком",
        "включи звук",
        "пробуждение",
        "проснись",
        "просыпайся",
        "верни звук",
        "стандартная громкость"
    ],
    "max_volume": [
        "громкость на максимум",
        "максимальная громкость",
    ],
    "volume_up": [
        "чуть выше громкость",
        "громкость чуть выше",
        "сделай громкость побольше",
        "сделай громкость повыше",
        "сделай чуть погромче"
    ],
    "volume_down": [
        "чуть ниже громкость",
        "громкость чуть ниже",
        "сделай громкость поменьше",
        "сделай громкость пониже",
        "сделай чуть потише"
    ],
    "turn_on_music": [
        "музыка",
        "музон",
        "музяка",
        "врубай",
        "включай музяку",
        "врубай музяку",
        "вруби музон",
        "врубай музыку",
        "вруби музыку",
        "включи музон",
        "включи музыку",
        "включай музыку"
    ],
    "stop_music": [
        "останови музыку",
        "прерви музыку",
        "приостанови музыку",
        "останови музон",
        "останови музяку",
        "прерви музяку",
        "прерви музон",
        "приостанови музяку"
    ],
    "play_music": [
        "возобнови музыку",
        "возобнови музяку",
        "возобнови музон",
        "возобнови музло",
    ],
    "change_music": [
        "смени музыку",
        "измени музыку"
    ],
    "loop_music": [
        "зацикли музон",
        "зацикли музяку",
        "зацикли музыку",
        "зацикли музло"
    ],
    "turn_off_music": [
        "тишина",
        "тихо",
        "выключай музяку",
        "выключи музыку",
        "выключай музыку",
        "выключи музон"
    ],
    "take_screenshot": [
        "сделай скриншот",
        "сделай снимок экрана",
        "скриншот",
        "снимок экрана"
    ],
    "get_geolocation": [
        "отследи устройство",
        "определи геолокацию",
        "определи текущее местоположение",
        "определи местоположение",
        "определи текущее местоположение устройства",
        "определи местоположение устройства"
    ],
    "get_battery_charge": [
        "определи заряд батареи",
        "определи остаток заряда батареи",
        "определи баратею",
        "сколько заряд",
        "сколько батареи",
        "какой заряд",
        "определи заряд"
    ],
    "lock_computer": [
        "заблокируй устройство",
        "заблокируй компьютер",
        "заблочь комп",
        "заблокируй доступ",
        "заблокируй экран",
        "заблочь экран",
        "блок"
    ],
    "computer_sleep": [
        "переведи компьютер в сон",
        "переведи компьютер в спящий режим",
        "компьютер в сон",
        "отправь компьютер в спящий режим",
        "отправь компьютер в спячку",
        "отключи компьютер",
        "отключи комп",
        "переведи устройство в сон",
        "переведи устройство в спящий режим",
        "устройство в сон",
        "отправь устройство в спящий режим",
        "отправь устройство в спячку",
        "отключи устройство"
    ],
    "poweroff": [
        "выключайся",
        "завершение работы",
        "выключись",
        "выключить",
        "выключить нахуй",
        "выключись нахуй",
        "закройся",
        "вырубись",
        "иди убейся"
    ]
}

# Links and file paths
TERRARIA_PATH: str = 'C:/GOG Games/Terraria/Terraria.exe'
TMODLOADER_PATH: str = '"C:/GOG Games/tModLoader/start-tModLoader.bat"'
MINECRAFT_PATH: str = "C:/Users/gleba/Desktop/Minecraft.exe"
TLAUNCHER_PATH: str = "C:/Users\gleba\AppData\Roaming\.minecraft\TLauncher.exe"
RELATIVE_VA_PATH: str = "app\modules\core\logic\main.py"
GOODBYE_DPI_PATH: str = "C:/Users/gleba/Desktop/goodbyedpi-0.2.3rc1-2/goodbyedpi-0.2.3rc1/1_russia_blacklist"
CHROME_PATH: str = "C:/Program Files/Google/Chrome/Application/chrome.exe"
GALLERY_PATH: str = "C:/Users/gleba/Desktop/Screenshots"
BASE_BROWSER: str = "google-chrome"
BASE_URL: str = "https://github.com/Gleb-a-p/NeuralWaifu" # "https://python.org"
YOUTUBE_URL: str = "https://www.youtube.com"
BASE_GPT_URL: str = "https://openrouter.ai/api/v1"
LOCALHOST_URL: str = "http://localhost:1234/v1"

# LLM Models
GPT_MODEL_LIST: list[str] = [
    "openai/gpt-4.1-mini",
    "deepseek/deepseek-r1-0528:free",
    "google/gemma-3n-e4b-it:free",
    "deepseek/deepseek-chat-v3-0324:free"
] # "gpt-o1-preview" # "gpt-3.5-turbo-1106"

GPT_FREE_MODEL_LIST: list[str] = [
    "gpt-3.5-turbo",
    "gpt-4o-mini",
    "gpt-4-turbo"
]

LMSTUDIO_MODEL: str = "deepseek-r1-0528-qwen3-8b"
# Available options:
#  - "deepseek-r1-distill-qwen-1.5b"
#  - /"deepseek-coder-6.7b-instruct"
#  - "deepseek-r1-0528-qwen3-8b"

OPTIONS_MESSAGE: str = (
    "Options:\n"
    "'b' - base mode\n"
    "(your API_KEY will be used), high quality\n"
    "'f' - free mode\n"
    "(your API_KEY won't be used, free model), low quality\n"
    "'lms' - lmstudio mode\n"
    "(uses the computing power of your computer, not recommended on a weak computer), \n"
    "quality is adjustable and depends on the local machine and choosed LLM model\n"
    "Please, select one of suggested options(b, f, lms): "
)

LLM_MODES = {
    'b': "base",
    'f': "free",
    'lms': "lmstudio"
}

MODE_CHOOSING_MESSAGE: str = "Please, select one from suggested VA's work modes: "

CHECKING_MESSAGE: str = "Кто ты?"

# Responses to commands
NOT_UNDERSTAND_ANSWER: str = "Команда не распознана."

JOKER_LIST: list[str] = [
    "Как смеются программисты? ... ехе.ехе.ехе",
    "Программист это машина для преобразования кофе в код.",
    "Я бы пошутил про химию, но боюсь реакции не будет, сэр.",
    "Палата умирающих комиков - это вам не шутки, сэр.",
    "Вы любите людей? Нет. Да ладно, все любят людей. А я нет. Вы просто не умеете их готовить.",
    "Почему химики не любят шутки? Они боятся реакции.",
    "Почему программисты не любят плавать? Потому что они всегда боятся утонуть в коде!",
    "Искуственный интелект никогда не ошибается, он экспериментирует.",
    "Почему ИИ всегда выглядит уверенно? Он знает, что у него есть 'дата' на каждый день!",
    "Почему программисты любят искусственный интеллект? Потому что он всегда учится на своих ошибках, а не просто забивает на них.",
    "По-моему, покупка вентилятора - это деньги на ветер.",
    "Черный юмор - это как вода в Африке. Она не до всех доходит."
]

TAKE_SCREENSHOT_ANSWER: str = "Снимок экрана сохранён"

# Probabilities and constants
OPERATION_SYSTEM: str = platform.platform()
"""
The percentage of probability with which a command
for an assistant is considered recognized.
"""
CMD_PERCENT_DETECTION: int = 55 # 50
"""
The percentage of probability with which
the assistant's name is considered recognized.
"""
NAME_PERCENT_DETECTION: int = 70
BASE_VOLUME: float = 0.66
BASE_VOLUME_UP: float = 0.05
BASE_VOLUME_DOWN: float = 0.05
DEVICE: int = 1  # recorder ID
DETECTING_SAMPLERATE: int = 16000
SYNTHESIS_SAMPLERATE: int = 48000
"""
Supported values for 'LANGUAGE' are:
    en (English, default)
    am (Amharic)
    ar (Arabic)
    az (Azerbaijani)
    be (Belarusian)
    bn (Bangladeshi)
    ca (Catalan)
    ce (Chechen)
    cs (Czech)
    cy (Welsh)
    da (Danish)
    de (German)
    en_GB (English - Great Britain)
    en_IN (English - India)
    en_NG (English - Nigeria)
    es (Spanish)
    es_CO (Spanish - Colombia)
    es_CR (Spanish - Costa Rica)
    es_GT (Spanish - Guatemala)
    es_VE (Spanish - Venezuela)
    eu (EURO)
    fa (Farsi)
    fi (Finnish)
    fr (French)
    fr_BE (French - Belgium)
    fr_CH (French - Switzerland)
    fr_DZ (French - Algeria)
    he (Hebrew)
    hu (Hungarian)
    id (Indonesian)
    is (Icelandic)
    it (Italian)
    ja (Japanese)
    kn (Kannada)
    ko (Korean)
    kz (Kazakh)
    lt (Lithuanian)
    lv (Latvian)
    nl (Dutch)
    no (Norwegian)
    pl (Polish)
    pt (Portuguese)
    pt_BR (Portuguese - Brazilian)
    ro (Romanian)
    ru (Russian)
    sl (Slovene)
    sk (Slovak)
    sr (Serbian)
    sv (Swedish)
    te (Telugu)
    tet (Tetum)
    tg (Tajik)
    tr (Turkish)
    th (Thai)
    uk (Ukrainian)
    vi (Vietnamese)
"""
VA_LANGUAGE: str = "ru"
SCREENSHOT_NAME: str = "Screenshot"
SCREENSHOT_EXTENSION: str = ".png"
