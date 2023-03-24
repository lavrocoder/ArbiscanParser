import requests
from bs4 import BeautifulSoup

from transfer import Transfers, Transfer


class Parser:
    def __init__(self, url: str):
        self.url = url
        self.html = self.get_html(self.url)
        self.soup = self.get_soup(self.html)

    @classmethod
    def get_html(cls, url):
        return requests.get(url).text

    @classmethod
    def get_soup(cls, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def get_transfers(self) -> Transfers:
        rows = self.soup.select("#tblResult > tbody > tr")
        transfers = []
        for row in rows:
            transfer = Transfer()

            txn_hash = row.select('td:nth-child(2)')
            transfer.txn_hash = txn_hash[0].text.strip() if txn_hash else None

            date_time_utc = row.select('td:nth-child(3)')
            transfer.date_time_utc = date_time_utc[0].text.strip() if date_time_utc else None

            address_from = row.select('td:nth-child(5)')
            transfer.address_from = address_from[0].text.strip() if address_from else None

            transfer_type = row.select('td:nth-child(6)')
            transfer.transfer_type = transfer_type[0].text.strip() if transfer_type else None

            address_to = row.select('td:nth-child(7)')
            transfer.address_to = address_to[0].text.strip() if address_to else None

            value = row.select('td:nth-child(8)')
            transfer.value = value[0].text.strip() if value else None

            token = row.select('td:nth-child(9)')
            transfer.token = token[0].text.strip() if token else None

            transfers.append(transfer)

        return Transfers(transfers)
