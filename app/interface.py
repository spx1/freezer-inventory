from typing import TypedDict
from datetime import date

class CategoryInterface(TypedDict, total=False):
    id: int
    name: str

class ItemInterface(TypedDict, total=False):
    id: int
    name: str
    category_id: int
    category : CategoryInterface
    weight: float
    count: int
    active: bool
    added: date
    removed: date

