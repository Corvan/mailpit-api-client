from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(init=True)
class Contact:
    Name: str = field(init=True)
    Address: str = field(init=True)