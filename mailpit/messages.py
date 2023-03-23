"""module containing everything related to messages"""
import dataclasses as dc

import typing
import dataclasses_json as dj

from . import models as m


@dj.dataclass_json
@dc.dataclass(init=True)
class Message:
    """
    class representing a single message that has been returned by the messages endpoint
    """

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-few-public-methods
    # pylint: disable=invalid-name

    id: str = dc.field(init=True, metadata=dj.config(field_name="ID"))
    read: bool = dc.field(init=True, metadata=dj.config(field_name="Read"))
    """always true (message marked read on open)"""
    from_: typing.Optional[m.Contact] = dc.field(
        init=True, metadata=dj.config(field_name="From")
    )
    to: list[m.Contact] = dc.field(init=True, metadata=dj.config(field_name="To"))
    cc: typing.Optional[list[m.Contact]] = dc.field(
        init=True, metadata=dj.config(field_name="Cc")
    )
    bcc: list[m.Contact] = dc.field(init=True, metadata=dj.config(field_name="Bcc"))
    subject: str = dc.field(init=True, metadata=dj.config(field_name="Subject"))
    """Message subject"""
    created: str = dc.field(init=True, metadata=dj.config(field_name="Created"))
    """Parsed email local date & time from headers"""
    size: int = dc.field(init=True, metadata=dj.config(field_name="Size"))
    """Total size of raw email"""
    attachments: int = dc.field(init=True, metadata=dj.config(field_name="Attachments"))


@dj.dataclass_json
@dc.dataclass(init=True)
class Messages:
    # pylint: disable=too-few-public-methods
    """
    class representing the returns of the messages endpoint
    """

    total: int = dc.field(init=True)
    """Total messages in mailbox"""
    unread: int = dc.field(init=True)
    """Total unread messages in mailbox"""
    count: int = dc.field(init=True)
    """Number of messages returned in request"""
    start: int = dc.field(init=True)
    """The offset (default=0) for pagination"""
    messages: list[Message]

    def __post_init__(self):
        if self.total < 0:
            raise ValueError("field 'total' may not be negative")
        if self.unread < 0:
            raise ValueError("field 'unread' may not be negative")
