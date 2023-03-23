"""module containing classes for the message-endpoint"""
import datetime
from typing import Optional

import dataclasses as dc
import dataclasses_json as dj

import mailpit.models as m


@dj.dataclass_json
@dc.dataclass(init=True)
class Attachment:
    """
    class representing an attachment of a message
    """

    # pylint: disable=too-few-public-methods

    part_id: str = dc.field(init=True, metadata=dj.config(field_name="PartID"))
    file_name: str = dc.field(init=True, metadata=dj.config(field_name="FileName"))
    content_type: str = dc.field(
        init=True, metadata=dj.config(field_name="ContentType")
    )
    content_id: str = dc.field(init=True, metadata=dj.config(field_name="ContentID"))
    size: int = dc.field(init=True, metadata=dj.config(field_name="Size"))


@dj.dataclass_json
@dc.dataclass(init=True)
class Message:
    """
    class representing a Message returned by the message-endpoint
    """

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-few-public-methods
    # pylint: disable=invalid-name

    read: bool = dc.field(init=True, metadata=dj.config(field_name="Read"))
    """always true (message marked read on open)"""
    from_: Optional[m.Contact] = dc.field(
        init=True, metadata=dj.config(field_name="From")
    )
    to: list[m.Contact] = dc.field(init=True, metadata=dj.config(field_name="To"))
    cc: Optional[list[m.Contact]] = dc.field(
        init=True, metadata=dj.config(field_name="Cc")
    )
    bcc: list[m.Contact] = dc.field(init=True, metadata=dj.config(field_name="Bcc"))
    subject: str = dc.field(init=True, metadata=dj.config(field_name="Subject"))
    """Message subject"""
    date: datetime.date = dc.field(init=True, metadata=dj.config(field_name="Date"))
    """Parsed email local date & time from headers"""
    text: Optional[str] = dc.field(init=True, metadata=dj.config(field_name="Text"))
    """Plain text MIME part of the email"""
    html: Optional[str] = dc.field(init=True, metadata=dj.config(field_name="HTML"))
    """HTML MIME part (if exists)"""
    size: int = dc.field(init=True, metadata=dj.config(field_name="Size"))
    """Total size of raw email"""
    inline: list[Attachment] = dc.field(
        init=True, metadata=dj.config(field_name="Inline")
    )
    attachments: list[Attachment] = dc.field(
        init=True, metadata=dj.config(field_name="Attachments")
    )
