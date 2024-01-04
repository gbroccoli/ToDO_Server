import os
import base64
import secrets


def generate_secret_key():
    # Генерировать случайный байтовый ключ
    key = secrets.token_bytes(32)
    return base64.b64encode(key).decode('utf-8')


def create_or_load_secret_key():
    # Путь к файлу .env (на два уровня выше относительно исполняемого скрипта)
    env_file_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            ".env"))
    secret_key = generate_secret_key()

    # Проверить, существует ли файл .env
    if os.path.isfile(env_file_path):
        with open(env_file_path, "r") as env_file:
            lines = env_file.readlines()

        with open(env_file_path, "w") as env_file:
            for line in lines:
                if line.startswith("APP_KEY="):
                    # Если строка начинается с "KEY=", заменить значение на
                    # сгенерированный секретный ключ
                    env_file.write(f"APP_KEY={secret_key}\n")
                else:
                    # В противном случае, оставить строку без изменений
                    env_file.write(line)

    else:
        # Если файла .env не существует, создать его и записать в него
        # сгенерированный секретный ключ
        with open(env_file_path, "w") as env_file:
            env_file.write(f"KEY={secret_key}\n")

    return secret_key


def main():
    # Получить или создать секретный ключ
    create_or_load_secret_key()

    # Использовать секретный ключ
    # print("Секретный ключ:", secret_key)


if __name__ == "__main__":
    main()
