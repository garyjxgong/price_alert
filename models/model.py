from typing import List, TypeVar, Type, Union
from common.database import Database
from abc import ABCMeta, abstractmethod

T = TypeVar('T', bound="Model")


class Model(metaclass=ABCMeta):
    collection: str
    _id: str

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def json(self) -> dict:
        raise NotImplementedError

    def save_to_mongo(self) -> None:
        Database.update(self.collection, {"_id": self._id}, self.json())

    def remove_from_mongo(self) -> None:
        Database.remove(self.collection, {"_id": self._id})

    @classmethod
    def get_by_id(cls: Type[T], _id: str) -> T:
        return cls(**Database.find_one(cls.collection, {"_id": _id}))

    @classmethod
    def all(cls: Type[T]) -> List[T]:
        elements_from_db = Database.find(cls.collection, {})
        return [cls(**ele) for ele in elements_from_db]

    @classmethod
    def find_one_by(cls: Type[T], attribute: str, value: Union[str, dict]) -> T:
        return cls(**Database.find_one(cls.collection, {attribute: value}))

    @classmethod
    def find_many_by(cls: Type[T], attribute: str, value: Union[str, dict]) -> List[T]:
        return [cls(**ele) for ele in Database.find(cls.collection, {attribute: value})]
