from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Item:
    name: str
    quantity: int
    image: str
