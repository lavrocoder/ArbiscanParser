import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_FILE_PATH = os.path.join(BASE_DIR, "config", "secret.json")

MAIN_TABLE = 'https://docs.google.com/spreadsheets/d/1kuEHhA6CZ8AQjQA6CsncjgdhTGJwBHMzOTvm_ULlNP8/edit#gid=0'
TIME_INTERVAL = 1 * 60
