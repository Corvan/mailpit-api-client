"""Definitions of model classes, that wrap Mailpit's API data-structures. Defined with 
:py:mod:`dataclasses` and :py:mod:`dataclasses_json`, in order to use them as json over 
the API and be used as objects in the Python domain."""
import dataclasses
import datetime
import decimal
import email.utils as email
import logging
import re
from typing import Optional, Iterable

import dataclasses_json
import marshmallow.fields


_log = logging.getLogger("mailpit_client")


@dataclasses_json.dataclass_json
@dataclasses.dataclass(init=True)
class Contact:
    """Represents a mail contact splitting 'Test User <test@example.com> into
    its name and address parts"""

    # pylint: disable=too-few-public-methods

    name: str = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="Name")
    )
    """Contact's Name"""
    address: str = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="Address")
    )
    """Contact's E-Mail address"""

    def __lt__(self, other):
        return f"{other.name} {other.address}".__lt__(f"{self.name} {self.address}")

    def __hash__(self):
        return f"{self.name} {self.address}".__hash__()


@dataclasses.dataclass(init=True)
class Attachment(dataclasses_json.DataClassJsonMixin):
    """Represents an attachment of a :py:class:`Message`"""

    # pylint: disable=too-few-public-methods

    part_id: str = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="PartID")
    )
    """Attachment's part ID"""
    file_name: str = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="FileName")
    )
    """Attachment's file name"""
    content_type: str = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="ContentType")
    )
    """Attachment's MIME content-type"""
    content_id: str = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="ContentID")
    )
    size: int = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="Size")
    )
    """Attachment's size in bytes"""

    def __lt__(self, other: "Attachment"):
        return (
            f"{other.part_id} {other.file_name} {other.content_type} "
            f"{other.content_id} {other.size}".__lt__(
                f"{self.part_id} {self.file_name} {self.content_type} "
                f"{self.content_id} {self.size}"
            )
        )

    def __hash__(self):
        return (
            f"{self.part_id} {self.file_name} {self.content_type} "
            f"{self.content_id} {self.size}"
        ).__hash__()


@dataclasses.dataclass(init=True)
class Message(dataclasses_json.DataClassJsonMixin):
    """Represents a message returned by the message-endpoint"""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-few-public-methods
    # pylint: disable=invalid-name

    id: str = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="ID")
    )
    """Message's database ID, of Mailpit's message-database"""
    message_id: str = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="MessageID")
    )
    """Message's RFC-5322 message-id"""
    read: bool = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="Read")
    )
    """Always true (message marked read on open)"""
    from_: Optional[Contact] = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="From")
    )
    """The :py:class`Contact`: the message is from"""
    to: list[Contact] = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="To")
    )
    """Message's To-Header, the list of :Contact: the message is addressed to"""
    cc: Optional[list[Contact]] = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="Cc")
    )
    """Message's CC-Header, the list of :Contact: that the message is coal-copied to"""
    bcc: Optional[list[Contact]] = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="Bcc")
    )
    """Message's BCC-Header, the list of :Contact:, that the message is blindly 
    coal-copied to"""
    subject: str = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="Subject")
    )
    """Message's subject"""
    date: datetime.date = dataclasses.field(
        init=True,
        metadata=dataclasses_json.config(
            field_name="Date",
            encoder=datetime.datetime.isoformat,
            decoder=datetime.datetime.fromisoformat,
            mm_field=marshmallow.fields.DateTime("iso"),
        ),
    )
    """Parsed email local date & time from headers"""
    text: Optional[str] = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="Text")
    )
    """Plain text MIME part of the email"""
    html: Optional[str] = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="HTML")
    )
    """HTML MIME part (if exists)"""
    size: int = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="Size")
    )
    """Total size of raw email in bytes"""
    inline: list[Attachment] = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="Inline")
    )
    """Inline Attachments"""
    attachments: list[Attachment] = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="Attachments")
    )
    """Attachments"""

    def __eq__(self, other):
        """check if a message is equal to another message. Fields not included are
        Mailpit's Database-ID because it might not be known and the size in bytes,
        because it might be differently depending on the way messages are saved

        :returns: :py:class:`True` if two messages are equal, :py:class:`False` if not
        """
        if not isinstance(other, Message):
            raise NotImplementedError
        if other is None:
            return False
        if other.message_id is None and self.message_id is not None:
            return False
        if other is not None and self.message_id is None:
            return False
        if other.message_id is not None and self.message_id is not None:
            if other.message_id != self.message_id:
                return False
        if other.from_ != self.from_:
            return False
        if other.subject != self.subject:
            return False
        if other.date != self.date:
            return False
        if other.text != self.text:
            return False
        if other.html != self.html:
            return False
        if set(sorted(other.to)).difference(sorted(self.to)):
            return False
        if (
            other.cc is None
            and self.cc is not None
            or other.cc is not None
            and self.cc is None
        ):
            return False
        if len(other.cc) != len(self.cc):
            return False
        if set(sorted(other.cc)).difference(sorted(self.cc)):
            return False
        if (
            other.bcc is None
            and self.bcc is not None
            or other.bcc is not None
            and self.bcc is None
        ):
            return False
        if len(other.bcc) != len(self.bcc):
            return False
        if set(sorted(other.bcc)).difference(sorted(self.bcc)) or set(
            sorted(self.bcc)
        ).difference(sorted(other.bcc)):
            return False
        if len(other.inline) != len(self.inline):
            return False
        if set(sorted(other.inline)).difference(sorted(self.inline)) or set(
            sorted(self.inline)
        ).difference(sorted(other.inline)):
            return False
        if len(other.attachments) != len(self.attachments):
            return False
        if set(sorted(other.attachments)).difference(sorted(self.attachments)) or set(
            sorted(self.attachments)
        ).difference(sorted(other.attachments)):
            return False
        return True


def datelist_encoder(encodes: Iterable[datetime.datetime]) -> list[str]:
    return list(map(lambda encode: email.format_datetime(encode), encodes))


def datelist_decoder(decodes: Iterable[str]) -> list[datetime.datetime]:
    return list(map(lambda decode: email.parsedate_to_datetime(decode), decodes))


@dataclasses_json.dataclass_json(undefined=dataclasses_json.Undefined.INCLUDE)
@dataclasses.dataclass(init=True)
class Headers:
    content_type: list[str] = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="Content-Type")
    )
    date: list[datetime.date] = dataclasses.field(
        init=True,
        metadata=dataclasses_json.config(
            field_name="Date",
            encoder=datelist_encoder,
            decoder=datelist_decoder,
            mm_field=marshmallow.fields.List(marshmallow.fields.DateTime("iso")),
        ),
    )
    delivered_to: list[str] = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="Delivered-To")
    )
    from_: list[str] = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="From")
    )
    message_id: list[str] = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="Message-Id")
    )
    additional: dataclasses_json.CatchAll = dataclasses.field(init=True)


def millis_to_3_digit(isoformat: str) -> str:
    """replaces milliseconds with
    three-digits long value using zero padding before"""
    millis = re.search(r"\.\d{0,3}", isoformat)
    if not millis:
        seconds = re.search(r":\d+(:\d+)", isoformat)
        _log.debug(f"seconds: {seconds}")
        if seconds is None:
            raise ValueError("seconds may not be None")
        return isoformat.replace(seconds.group(0), f"{seconds.group(0)}.000")
    _log.debug(f"millis: {millis.group(0)}, {decimal.Decimal(millis.group(0)):.03f}")
    return isoformat.replace(
        f"{millis.group(0)}", f".{int(decimal.Decimal(millis.group(0)) * 1000):03}"
    )


def zulu_to_utc_shift(isoformat: str) -> str:
    """replaces 'Z' with '+00:00' for UTC"""
    return isoformat.replace("Z", "+00:00")


def datetime_decoder(isoformat: str) -> datetime.datetime:
    """replaces golang isoformat with Python parsable isoformat
    and decodes it to `datetime.datetime`"""
    _log.debug(f"old isdoformat: {isoformat}")

    result = zulu_to_utc_shift(millis_to_3_digit(isoformat))
    _log.debug(f"new isoformat: {result}")
    return datetime.datetime.fromisoformat(result)


@dataclasses.dataclass(init=True)
class MessageSummary(dataclasses_json.DataClassJsonMixin):
    """class representing a single message that has been returned by the messages
    endpoint"""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-few-public-methods
    # pylint: disable=invalid-name

    id: str = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="ID")
    )
    message_id: str = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="MessageID")
    )
    read: bool = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="Read")
    )
    """always true (message marked read on open)"""
    from_: Optional[Contact] = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="From")
    )
    to: list[Contact] = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="To")
    )
    cc: Optional[list[Contact]] = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="Cc")
    )
    bcc: list[Contact] = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="Bcc")
    )
    subject: str = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="Subject")
    )
    """Message subject"""
    created: datetime.date = dataclasses.field(
        init=True,
        metadata=dataclasses_json.config(
            field_name="Created",
            encoder=datetime.datetime.isoformat,
            decoder=datetime_decoder,
            mm_field=marshmallow.fields.DateTime("iso"),
        ),
    )
    """Parsed email local date & time from headers"""
    size: int = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="Size")
    )
    """Total size of raw email"""
    attachments: int = dataclasses.field(
        init=True, metadata=dataclasses_json.config(field_name="Attachments")
    )


@dataclasses.dataclass(init=True)
class Messages(dataclasses_json.DataClassJsonMixin):
    # pylint: disable=too-few-public-methods
    """class representing the returns of the messages endpoint"""

    total: int = dataclasses.field(init=True)
    """Total messages in mailbox"""
    unread: int = dataclasses.field(init=True)
    """Total unread messages in mailbox"""
    count: int = dataclasses.field(init=True)
    """Number of messages returned in request"""
    start: int = dataclasses.field(init=True)
    """The offset (default=0) for pagination"""
    messages: list[MessageSummary]

    def __post_init__(self):
        if self.total < 0:
            raise ValueError("field 'total' may not be negative")
        if self.unread < 0:
            raise ValueError("field 'unread' may not be negative")
