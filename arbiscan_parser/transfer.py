from __future__ import annotations
import json


class Transfers:
    def __init__(self, transfers=None):
        if transfers is None:
            transfers = []
        self.transfers = transfers

    def filter(self, **kwargs) -> list[Transfer]:
        transfers = []
        for transfer in self.transfers:
            try:
                if all([transfer.__getattribute__(key) == value for key, value in kwargs.items()]):
                    transfers.append(transfer)
            except AttributeError:
                pass
        return transfers


class Transfer:
    txn_hash: str
    date_time_utc: str
    address_from: str
    transfer_type: str
    address_to: str
    value: str
    token: str

    def to_json(self):
        object_json = {}
        for annotation in self.__annotations__:
            object_json.update({
                annotation: str(self.__getattribute__(annotation))
            })
        return object_json

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()
