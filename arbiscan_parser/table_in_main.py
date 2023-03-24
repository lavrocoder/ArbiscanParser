from __future__ import annotations


class TableInMain:
    name: str
    url: str
    status: str
    address: str

    # Фильтры
    txn_hash: str | None
    date_time: str | None
    from_address: str | None
    type_transfer: str | None
    to: str | None
    value: str | None
    token: str | None

    @classmethod
    def get_from_list(cls, table_list: list[str]) -> TableInMain:
        """
        Создает объект таблицы на основе строки из основной таблицы.
        :param table_list: Строка таблицы.
        :return: Объект таблицы.
        """
        table = cls()
        for i, attr in enumerate(cls.__annotations__):
            if table_list[i] == '':
                table.__setattr__(attr, None)
            else:
                table.__setattr__(attr, table_list[i])
        return table

    def get_filters(self) -> dict:
        """
        Собирает фильтры.
        :return: Фильтры в формате словаря.
        """
        filters = {}

        if self.txn_hash is not None:
            filters.update({'txn_hash': self.txn_hash})

        if self.date_time is not None:
            filters.update({'date_time_utc': self.date_time})

        if self.from_address is not None:
            filters.update({'from': self.from_address})

        if self.type_transfer is not None:
            filters.update({'type': self.type_transfer})

        if self.to is not None:
            filters.update({'to': self.to})

        if self.value is not None:
            filters.update({'value': self.value})

        if self.token is not None:
            filters.update({'token': self.token})

        return filters
