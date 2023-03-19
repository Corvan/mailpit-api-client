"""module containing everything related to messages"""
import typing
import dataclasses as dc
import dataclasses_json as dj
import requests as r
import mailpit.models as models


@dj.dataclass_json
@dc.dataclass(init=True)
class Message:
    id: str = dc.field(init=True, metadata=dj.config(field_name="ID"))
    read: bool = dc.field(init=True, metadata=dj.config(field_name="Read"))
    """always true (message marked read on open)"""
    from_: typing.Optional[models.Contact] = dc.field(
        init=True, metadata=dj.config(field_name="From")
    )
    to: list[models.Contact] = dc.field(init=True, metadata=dj.config(field_name="To"))
    cc: typing.Optional[list[models.Contact]] = dc.field(
        init=True, metadata=dj.config(field_name="Cc")
    )
    bcc: list[models.Contact] = dc.field(
        init=True, metadata=dj.config(field_name="Bcc")
    )
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

def get_messages(limit: int, start: int) -> Messages:
