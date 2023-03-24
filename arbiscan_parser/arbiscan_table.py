import gspread
from loguru import logger

from config import settings


class ArbiscanTable:
    def __init__(self, url: str):
        logger.info(f"Подключение к таблице {url}")
        self.service_account = gspread.service_account(settings.SECRET_FILE_PATH)
        self.table = self.service_account.open_by_url(url)
        self.sheet = self.table.worksheet('Token Transfers')

    def get_last_date(self) -> str | None:
        """
        Получает последнюю сохраненную дату из таблицы.
        :return: Строка даты. None если таблица пуста.
        """
        logger.info(f"Получение последней сохраненной даты в таблице")
        last_date = self.sheet.acell('B2').value
        return last_date

    def save_transfers(self, transfers: list[dict]):
        logger.info(f"Сохранение новых транзакций в таблицу")
        rows = [list(transfer.values()) for transfer in transfers]
        self.sheet.insert_rows(
            rows,
            2
        )
