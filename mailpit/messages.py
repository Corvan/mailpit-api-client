from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
import datetime
from mailpit.models import Contact
from typing import Optional


@dataclass_json
@dataclass(init=True)
class Message:

    Read: bool = field(init=True)
    """always true (message marked read on open)"""
    From: Optional[Contact] = field(init=True)
    To: list[Contact] = field(init=True)
    Cc: Optional[list[Contact]] = field(init=True)
    Bcc: list[Contact] = field(init=True)
    Subject: str = field(init=True)
    """Message subject"""
    Created: datetime.date = field(init=True)
    """Parsed email local date & time from headers"""
    Size: int = field(init=True)
    """Total size of raw email"""
    Attachments: int = field(init=True)


@dataclass_json
@dataclass(init=True)
class Messages:

    total: int = field(init=True)
    """Total messages in mailbox"""
    unread: int = field(init=True)
    """Total unread messages in mailbox"""
    count: int = field(init=True)
    """Number of messages returned in request"""
    start: int = field(init=True)
    """The offset (default=0) for pagination"""
    messages: list[Message]

    def __post_init__(self):
        if self.total < 0:
            raise ValueError("field 'total' may not be negative")
        if self.unread < 0:
            raise ValueError("field 'unread' may not be negative")
