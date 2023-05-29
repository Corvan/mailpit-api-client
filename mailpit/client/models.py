from __future__ import annotations
import dataclasses as _dc
import datetime as _dt
import decimal as _d
import email.utils as _email
import logging
import re as _re
from typing import Optional, Iterable

import dataclasses_json as _dj
import marshmallow.fields


_log = logging.getLogger("mailpit_client")


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


@_dc.dataclass(init=True)
class Attachment(_dj.DataClassJsonMixin):
    """
    class representing an attachment of a message
    """

    # pylint: disable=too-few-public-methods

    part_id: str = _dc.field(init=True, metadata=_dj.config(field_name="PartID"))
    file_name: str = _dc.field(init=True, metadata=_dj.config(field_name="FileName"))
    content_type: str = _dc.field(
        init=True, metadata=_dj.config(field_name="ContentType")
    )
    content_id: str = _dc.field(init=True, metadata=_dj.config(field_name="ContentID"))
    size: int = _dc.field(init=True, metadata=_dj.config(field_name="Size"))


@_dc.dataclass(init=True)
class Message(_dj.DataClassJsonMixin):
    """
    class representing a Message returned by the message-endpoint
    """

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-few-public-methods
    # pylint: disable=invalid-name

    id: str = _dc.field(init=True, metadata=_dj.config(field_name="ID"))
    message_id: str = _dc.field(init=True, metadata=_dj.config(field_name="MessageID"))
    read: bool = _dc.field(init=True, metadata=_dj.config(field_name="Read"))
    """always true (message marked read on open)"""
    from_: Optional[Contact] = _dc.field(
        init=True, metadata=_dj.config(field_name="From")
    )
    to: list[Contact] = _dc.field(init=True, metadata=_dj.config(field_name="To"))
    cc: Optional[list[Contact]] = _dc.field(
        init=True, metadata=_dj.config(field_name="Cc")
    )
    bcc: list[Contact] = _dc.field(init=True, metadata=_dj.config(field_name="Bcc"))
    subject: str = _dc.field(init=True, metadata=_dj.config(field_name="Subject"))
    """Message subject"""
    date: _dt.date = _dc.field(
        init=True,
        metadata=_dj.config(
            field_name="Date",
            encoder=_dt.datetime.isoformat,
            decoder=_dt.datetime.fromisoformat,
            mm_field=marshmallow.fields.DateTime("iso"),
        ),
    )
    """Parsed email local date & time from headers"""
    text: Optional[str] = _dc.field(init=True, metadata=_dj.config(field_name="Text"))
    """Plain text MIME part of the email"""
    html: Optional[str] = _dc.field(init=True, metadata=_dj.config(field_name="HTML"))
    """HTML MIME part (if exists)"""
    size: int = _dc.field(init=True, metadata=_dj.config(field_name="Size"))
    """Total size of raw email"""
    inline: list[Attachment] = _dc.field(
        init=True, metadata=_dj.config(field_name="Inline")
    )
    attachments: list[Attachment] = _dc.field(
        init=True, metadata=_dj.config(field_name="Attachments")
    )


def _datelist_encoder(encodes: Iterable[_dt.datetime]) -> list[str]:
    return list(map(lambda encode: _email.format_datetime(encode), encodes))


def _datelist_decoder(decodes: Iterable[str]) -> list[_dt.datetime]:
    return list(map(lambda decode: _email.parsedate_to_datetime(decode), decodes))


@_dj.dataclass_json(undefined=_dj.Undefined.INCLUDE)
@_dc.dataclass(init=True)
class Headers:
    content_type: list[str] = _dc.field(
        init=True, metadata=_dj.config(field_name="Content-Type")
    )
    date: list[_dt.date] = _dc.field(
        init=True,
        metadata=_dj.config(
            field_name="Date",
            encoder=_datelist_encoder,
            decoder=_datelist_decoder,
            mm_field=marshmallow.fields.List(marshmallow.fields.DateTime("iso")),
        ),
    )
    delivered_to: list[str] = _dc.field(
        init=True, metadata=_dj.config(field_name="Delivered-To")
    )
    from_: list[str] = _dc.field(init=True, metadata=_dj.config(field_name="From"))
    message_id: list[str] = _dc.field(
        init=True, metadata=_dj.config(field_name="Message-Id")
    )
    additional: _dj.CatchAll = _dc.field(init=True)


def millis_to_3_digit(isoformat: str) -> str:
    """replaces milliseconds with
    three-digits long value using zero padding before"""
    millis = _re.search(r"\.\d{0,3}", isoformat)
    if not millis:
        raise ValueError("No milliseconds provided in isoformat string")
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


@_dc.dataclass(init=True)
class MessageSummary(_dj.DataClassJsonMixin):
    """
    class representing a single message that has been returned by the messages endpoint
    """

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-few-public-methods
    # pylint: disable=invalid-name

    id: str = _dc.field(init=True, metadata=_dj.config(field_name="ID"))
    read: bool = _dc.field(init=True, metadata=_dj.config(field_name="Read"))
    """always true (message marked read on open)"""
    from_: Optional[Contact] = _dc.field(
        init=True, metadata=_dj.config(field_name="From")
    )
    to: list[Contact] = _dc.field(init=True, metadata=_dj.config(field_name="To"))
    cc: Optional[list[Contact]] = _dc.field(
        init=True, metadata=_dj.config(field_name="Cc")
    )
    bcc: list[Contact] = _dc.field(init=True, metadata=_dj.config(field_name="Bcc"))
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


@_dc.dataclass(init=True)
class Messages(_dj.DataClassJsonMixin):
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
    messages: list[MessageSummary]

    def __post_init__(self):
        if self.total < 0:
            raise ValueError("field 'total' may not be negative")
        if self.unread < 0:
            raise ValueError("field 'unread' may not be negative")
