"""module containing shared model classes"""
import dataclasses as _dc

import dataclasses_json as _dj


@_dj.dataclass_json
@_dc.dataclass(init=True)
class Contact:
    """
    class representing a mail contact splitting 'Test User <test@example.com> into
    its name and address parts
    """

    # pylint: disable=too-few-public-methods

    name: str = _dc.field(init=True, metadata=_dj.config(field_name="Name"))
    address: str = _dc.field(init=True, metadata=_dj.config(field_name="Address"))
