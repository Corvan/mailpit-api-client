"""module containing shared model classes"""
import dataclasses as dc

import dataclasses_json as dj


@dj.dataclass_json
@dc.dataclass(init=True)
class Contact:
    """
    class representing a mail contact splitting 'Test User <test@example.com> into
    its name and address parts
    """

    # pylint: disable=too-few-public-methods

    name: str = dc.field(init=True, metadata=dj.config(field_name="Name"))
    address: str = dc.field(init=True, metadata=dj.config(field_name="Address"))
