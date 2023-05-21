"""module containing classes for the message-endpoint"""
import datetime as _dt
from typing import Optional

import dataclasses as _dc
import dataclasses_json as _dj
import marshmallow.fields

import mailpit.client.models as _c_models


@_dj.dataclass_json
@_dc.dataclass(init=True)
class Attachment:
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


@_dj.dataclass_json
@_dc.dataclass(init=True)
class Message:
    """
    class representing a Message returned by the message-endpoint
    """

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-few-public-methods
    # pylint: disable=invalid-name

    id: str = _dc.field(init=True, metadata=_dj.config(field_name="ID"))
    read: bool = _dc.field(init=True, metadata=_dj.config(field_name="Read"))
    """always true (message marked read on open)"""
    from_: Optional[_c_models.Contact] = _dc.field(
        init=True, metadata=_dj.config(field_name="From")
    )
    to: list[_c_models.Contact] = _dc.field(
        init=True, metadata=_dj.config(field_name="To")
    )
    cc: Optional[list[_c_models.Contact]] = _dc.field(
        init=True, metadata=_dj.config(field_name="Cc")
    )
    bcc: list[_c_models.Contact] = _dc.field(
        init=True, metadata=_dj.config(field_name="Bcc")
    )
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