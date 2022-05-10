from abc import abstractmethod
from collections import OrderedDict

from model import Item
from typing import Tuple, Generator, List, Dict

_instance = None


class Database(object):

    def __new__(cls):
        global _instance
        if _instance is None:
            _instance = super(Database, cls).__new__(cls)
        return _instance

    @classmethod
    def get_instance(cls):
        return _instance

    @abstractmethod
    async def add_item(self, i: Item) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_item(self, _id: int) -> Item:
        """
        :param _id: The Item ID

        :raises
            KeyError: In case the item does not exist

        :return: The actual Item
        """
        raise NotImplementedError

    @abstractmethod
    async def update_item(self, _id: int, i: Item) -> None:
        """
        :param _id: The Item ID to update
        :param i: The new Item

        :raises
            KeyError: In case the item does not exist
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_item(self, _id: int, reason: str) -> None:
        """
        :param _id: The Item ID to delete
        :param reason: The reason for Item deletion

        :raises
            KeyError: In case the item does not exist
        """
        raise NotImplementedError

    @abstractmethod
    async def list_items(self) -> Generator[Tuple[int, Item], None, None]:
        raise NotImplementedError

    @abstractmethod
    async def list_deleted_items(self) -> Generator[Tuple[int, Dict[Item, str]], None, None]:
        raise NotImplementedError

    @abstractmethod
    async def undelete(self, _id: int) -> None:
        """
        :raises
            KeyError: In case the item does not exist or not deleted
        """
        raise NotImplementedError


class InMemoryDB(Database):
    # a persistent database is not a requirement, but can be implemented
    def __init__(self):
        self.__internal_dict = OrderedDict()  # type: OrderedDict[int, Item]
        self.__deleted_items = []  # type: List[Tuple[int, Item, str]]

    async def add_item(self, i: Item) -> int:
        _id = len(self.__internal_dict)
        self.__internal_dict[_id] = i
        return _id

    async def get_item(self, _id: int) -> Item:
        return self.__internal_dict[_id]

    async def update_item(self, _id: int, i: Item) -> None:
        self.__internal_dict[_id] = i

    async def delete_item(self, _id: int, reason: str) -> None:
        self.__deleted_items.append((_id, self.__internal_dict[_id], reason))
        del self.__internal_dict[_id]

    async def list_items(self) -> Generator[Tuple[int, Item], None, None]:
        for k, v in self.__internal_dict.items():
            yield k, v

    async def list_deleted_items(self) -> Generator[Tuple[int, Dict[Item, str]], None, None]:
        for _id, item, reason in self.__deleted_items:
            yield _id, {
                "item": item,
                "reason": reason,
            }

    async def undelete(self, _id: int) -> None:
        to_remove = None
        for index, (__id, item, reason) in enumerate(self.__deleted_items):
            if __id == _id:
                self.__internal_dict[__id] = item
                to_remove = index
                break
        if to_remove is None:
            raise KeyError
        # afaik we can't just delete this while iterating, better be safe
        del self.__deleted_items[to_remove]
