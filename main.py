import os
import time
import traceback

import gspread
from loguru import logger

from arbiscan_parser import utils
from config import settings


def main():
    log_path = os.path.join(
        settings.BASE_DIR, 'logs', 'arbiscan_parser_{time}.log'
    )
    logger.add(log_path)
    while True:
        t0 = time.time()
        try:
            tables = utils.get_tables_from_main_table()
        except gspread.exceptions.APIError as e:
            code = e.args[0].get('code')
            if code == 403:
                logger.warning('Нет доступа к основной таблице')
                logger.warning(
                    f'Укажите в настройках доступа основной таблицы "{utils.get_client_email_from_secret()}" редактором'
                )
                time.sleep(1)
                input("Нажмите Enter, чтобы выйти из программы")
                exit(1)
            else:
                raise e
        except Exception as e:
            logger.error('Произошла неизвестная ошибка при подключении к основной таблице')
            logger.warning(f"{e}")
            logger.warning(traceback.format_exc())
            time.sleep(1)
            input("Нажмите Enter, чтобы выйти из программы")
            exit(1)
        else:
            for i, table in enumerate(tables):
                status = utils.update_table(table)
                utils.set_status_for_main_table(status, i + 2)
                time.sleep(2)

        utils.time_interval(t0)


if __name__ == '__main__':
    main()
