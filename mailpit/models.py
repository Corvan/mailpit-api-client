from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass(init=True)
class Contact:
    name: str = field(init=True, metadata=config(field_name="Name"))
    address: str = field(init=True, metadata=config(field_name="Address"))
