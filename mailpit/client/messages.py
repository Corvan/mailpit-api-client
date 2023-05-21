"""module containing everything related to messages"""
from __future__ import annotations
import datetime as _dt
import decimal as _d
import logging
import typing

import re as _re

import dataclasses as _dc
import dataclasses_json as _dj
import marshmallow

import mailpit.client.models as _c_models


_log = logging.getLogger("mailpit_client")


def millis_to_3_digit(isoformat: str) -> str:
    """replaces milliseconds with
    three-digits long value using zero padding before"""
    millis = _re.search(r"\.\d{0,3}", isoformat)
    _log.debug(f"millis: {millis.group(0)}, {_d.Decimal(millis.group(0)):.03f}")
    return isoformat.replace(
        f"{millis.group(0)}", f".{int(_d.Decimal(millis.group(0)) * 1000):03}"
    )


def zulu_to_utc_shift(isoformat: str) -> str:
    """replaces 'Z' with '+00:00' for UTC"""
    return isoformat.replace("Z", "+00:00")


def datetime_decoder(isoformat: str) -> _dt.datetime:
    """replaces golang isoformat with Python parsable isoformat
    and decodes it to `datetime.datetime`"""
    _log.debug(f"old isdoformat: {isoformat}")

    result = zulu_to_utc_shift(millis_to_3_digit(isoformat))
    _log.debug(f"new isoformat: {result}")
    return _dt.datetime.fromisoformat(result)


@_dj.dataclass_json
@_dc.dataclass(init=True)
class Message:
    """
    class representing a single message that has been returned by the messages endpoint
    """

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-few-public-methods
    # pylint: disable=invalid-name

    id: str = _dc.field(init=True, metadata=_dj.config(field_name="ID"))
    read: bool = _dc.field(init=True, metadata=_dj.config(field_name="Read"))
    """always true (message marked read on open)"""
    from_: typing.Optional[_c_models.Contact] = _dc.field(
        init=True, metadata=_dj.config(field_name="From")
    )
    to: list[_c_models.Contact] = _dc.field(
        init=True, metadata=_dj.config(field_name="To")
    )
    cc: typing.Optional[list[_c_models.Contact]] = _dc.field(
        init=True, metadata=_dj.config(field_name="Cc")
    )
    bcc: list[_c_models.Contact] = _dc.field(
        init=True, metadata=_dj.config(field_name="Bcc")
    )
    subject: str = _dc.field(init=True, metadata=_dj.config(field_name="Subject"))
    """Message subject"""
    created: _dt.date = _dc.field(
        init=True,
        metadata=_dj.config(
            field_name="Created",
            encoder=_dt.datetime.isoformat,
            decoder=datetime_decoder,
            mm_field=marshmallow.fields.DateTime("iso"),
        ),
    )
    """Parsed email local date & time from headers"""
    size: int = _dc.field(init=True, metadata=_dj.config(field_name="Size"))
    """Total size of raw email"""
    attachments: int = _dc.field(
        init=True, metadata=_dj.config(field_name="Attachments")
    )


@_dj.dataclass_json
@_dc.dataclass(init=True)
class Messages:
    # pylint: disable=too-few-public-methods
    """
    class representing the returns of the messages endpoint
    """

    total: int = _dc.field(init=True)
    """Total messages in mailbox"""
    unread: int = _dc.field(init=True)
    """Total unread messages in mailbox"""
    count: int = _dc.field(init=True)
    """Number of messages returned in request"""
    start: int = _dc.field(init=True)
    """The offset (default=0) for pagination"""
    messages: list[Message]

    def __post_init__(self):
        if self.total < 0:
            raise ValueError("field 'total' may not be negative")
        if self.unread < 0:
            raise ValueError("field 'unread' may not be negative")
