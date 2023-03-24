import datetime
import json
import time
import traceback

import gspread
from loguru import logger

from arbiscan_parser.arbiscan import Arbiscan
from arbiscan_parser.table_in_main import TableInMain
from arbiscan_parser.arbiscan_table import ArbiscanTable
from config import settings


def transfers_filter(transfers: list[dict], **kwargs):
    items = []
    for transfer in transfers:
        if all([transfer[key] == value for key, value in kwargs.items()]):
            items.append(transfer)

    return items


def get_client_email_from_secret():
    """
    Получает email сервисного аккаунта из secret файла.
    :return: Email сервисного аккаунта.
    """
    with open(settings.SECRET_FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    return data.get('client_email')


def get_tables_from_main_table() -> list[TableInMain]:
    url = settings.MAIN_TABLE
    logger.info(f"Подключение к основной таблице {url}")
    service_account = gspread.service_account(settings.SECRET_FILE_PATH)
    main_table = service_account.open_by_url(url)
    sheet = main_table.worksheet('Таблицы')
    rows = sheet.get_values()
    tables = []
    for row in rows[1:]:
        table = TableInMain.get_from_list(row)
        tables.append(table)
    return tables


def update_table(table: TableInMain) -> str:
    """
    Обновляет данные в таблице Arbiscan на основе парсинга.
    :param table: Объект таблицы.
    :return: Статус обновления.
    """
    logger.info(f"Обновление данных таблицы {table.name} ({table.url})")
    try:
        arbiscan_table = ArbiscanTable(url=table.url)
    except gspread.exceptions.APIError as e:
        code = e.args[0].get('code')
        if code == 403:
            client_email = get_client_email_from_secret()
            logger.warning('Нет доступа к таблице')
            logger.warning(
                f'Укажите в настройках доступа таблицы "{client_email}" редактором'
            )
            status = f'Нет доступа к таблице\n' \
                     f'Укажите в настройках доступа таблицы "{client_email}" редактором'
        else:
            raise e
    except Exception as e:
        logger.error('Произошла неизвестная ошибка')
        logger.warning(f"{e}")
        status = f"{e}"
        logger.warning(traceback.format_exc())
    else:
        try:
            last_date = arbiscan_table.get_last_date()
            arbiscan = Arbiscan(table.address)
            transfers = arbiscan.parse_after_date_time(last_date)
            transfers = transfers_filter(transfers, **table.get_filters())
            arbiscan_table.save_transfers(transfers)
        except Exception as e:
            logger.error('Произошла неизвестная ошибка')
            logger.warning(f"{e}")
            status = f"{e}"
            logger.warning(traceback.format_exc())
        else:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            status = f'Обновлено {now}'
    return status


def set_status_for_main_table(status: str, row_index: int):
    """
    Обновляет статус таблицы в основной таблице.
    :param status: Статус.
    :param row_index: Индекс строки таблицы.
    """
    try:
        logger.info("Обновление статуса")
        url = settings.MAIN_TABLE
        service_account = gspread.service_account(settings.SECRET_FILE_PATH)
        main_table = service_account.open_by_url(url)
        sheet = main_table.worksheet('Таблицы')
        sheet.update_cell(row_index, 3, status)
    except Exception as e:
        logger.error('Произошла неизвестная ошибка')
        logger.warning(f"{e}")
        logger.warning(traceback.format_exc())


def time_interval(t0):
    t1 = t0 + settings.TIME_INTERVAL
    sleep = t1 - time.time()
    if sleep > 0:
        logger.info(f"Пауза {int(sleep)} с")
        time.sleep(sleep)
