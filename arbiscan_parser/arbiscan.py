import requests
from bs4 import BeautifulSoup
from loguru import logger


class Arbiscan:
    def __init__(self, address: str):
        """
        :param address: Адрес кошелька.
        """
        self.address = address

    def parse_page(self, page: int = 1) -> dict:
        """
        Получает список транзакций.
        :param page: Номер страницы для парсинга.
        :return: Словарь данных:
            * count_pages - количество страниц.
            * items - список транзакций:
                * txn_hash - поле из столбца 'Txn Hash'.
                * date_time_utc - поле из столбца 'Date Time (UTC)'.
                * from - поле из столбца 'From'.
                * type - поле из неподписанного столбца 'Type'.
                * to - поле из столбца 'To'.
                * value - поле из столбца 'Value'.
                * token - поле из столбца 'Token'.
        """
        logger.info(f"Парсинг страницы {page}")
        url = f'https://arbiscan.io/tokentxns?a={self.address}&p={page}'
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')

        count_pages = int(soup.select('.page-link > strong')[-1].text.strip())

        rows = soup.select("#tblResult > tbody > tr")
        items = []
        for row in rows:
            transfer = {
                "txn_hash": row.select('td:nth-child(2)')[0].text.strip(),
                "date_time_utc": row.select('td:nth-child(3)')[0].text.strip(),
                "from": row.select('td:nth-child(5)')[0].text.strip(),
                "type": row.select('td:nth-child(6)')[0].text.strip(),
                "to": row.select('td:nth-child(7)')[0].text.strip(),
                "value": row.select('td:nth-child(8)')[0].text.strip(),
                "token": row.select('td:nth-child(9)')[0].text.strip(),
            }
            items.append(transfer)

        result = {
            "count_pages": count_pages,
            "items": items
        }
        return result

    def parse_all(self) -> list[dict]:
        """
        Получает список транзакций со всех страниц.
        :return: Список транзакций:
            * txn_hash - поле из столбца 'Txn Hash'.
            * date_time_utc - поле из столбца 'Date Time (UTC)'.
            * from - поле из столбца 'From'.
            * type - поле из неподписанного столбца 'Type'.
            * to - поле из столбца 'To'.
            * value - поле из столбца 'Value'.
            * token - поле из столбца 'Token'.
        """
        items = []
        result = self.parse_page()
        items.extend(result.get('items'))
        for page in range(1, result.get('count_pages')):
            page = page + 1
            result = self.parse_page(page)
            items.extend(result.get('items'))
        return items

    def parse_after_date_time(self, after_date_time: str = None) -> list[dict]:
        """
        Получает список транзакций.
        :param after_date_time: Дата транзакции, до которой идет парсинг.
        :return: Список транзакций:
            * txn_hash - поле из столбца 'Txn Hash'.
            * date_time_utc - поле из столбца 'Date Time (UTC)'.
            * from - поле из столбца 'From'.
            * type - поле из неподписанного столбца 'Type'.
            * to - поле из столбца 'To'.
            * value - поле из столбца 'Value'.
            * token - поле из столбца 'Token'.
        """
        logger.info("Получение данных из Arbiscan")
        if after_date_time is None:
            return self.parse_all()
        items = []
        result = self.parse_page()
        for item in result.get('items'):
            if item.get('date_time_utc') <= after_date_time:
                return items
            else:
                items.append(item)
        for page in range(1, result.get('count_pages')):
            page = page + 1
            result = self.parse_page(page)
            for item in result.get('items'):
                if item.get('date_time_utc') <= after_date_time:
                    return items
                else:
                    items.append(item)
        return items
