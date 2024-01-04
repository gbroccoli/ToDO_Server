import re

def check_password_strength(password):
    """
    Функция для проверки сложности пароля.

    Args:
    password (str): Пароль для проверки.

    Returns:
    bool: True если пароль сильный, иначе False.
    """
    # Проверка длины пароля
    if len(password) < 12:
        return False

    # Проверка наличия заглавной буквы
    if not re.search(r"[A-Z]", password):
        return False

    # Проверка наличия строчной буквы
    if not re.search(r"[a-z]", password):
        return False

    # Проверка наличия цифры
    if not re.search(r"\d", password):
        return False

    # Проверка наличия специального символа
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False

    return True