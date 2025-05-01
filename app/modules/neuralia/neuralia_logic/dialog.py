# Приветственное сообщение
GREETING_MESSAGE = """Приветствую!
Меня зовут Нейро-тян, я текстовый и голосовой компьютерный помощник!
Всегда рада помочь!"""
REGISTRATION_MESSAGE = "Введите свое имя для дальнейшего обращения: "

# Настройки цвета для темной темы
BG_COLOR = "#2e2e2e"  # Темный фон
FG_COLOR = "#ffffff"  # Белый текст


def send_greeting_message(tk):
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, GREETING_MESSAGE)
    chat_log.config(state=tk.DISABLED)


def user_registration(entry, chat_log, tk):
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, REGISTRATION_MESSAGE)
    chat_log.config(state=tk.DISABLED)
    user_name = entry.get()
    return user_name


def send_message(entry, chat_log, tk, time, user_name="User"):
    # Получаем текст из поля ввода
    user_message = entry.get()
    
    # Добавляем сообщение пользователя в текстовое поле чата
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, f"{user_name}: {user_message}\n")
    chat_log.config(state=tk.DISABLED)
    
    # Очищаем поле ввода
    entry.delete(0, tk.END)
    
    # Генерируем ответ компьютера
    if user_message == "exit":
        computer_message = "Компьютер: Досвидания!\n"
    else:
        computer_message = "Компьютер: Спасибо за ваше сообщение!\n"
    
    # Добавляем ответ Нейралии в текстовое поле чата
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, computer_message)
    chat_log.config(state=tk.DISABLED)
    
    # Автоматическая прокрутка вниз
    chat_log.yview(tk.END)
    
    # Проверка на команду выхода из диалога
    if user_message == "exit":
        time.sleep(1)
        exit(0)
