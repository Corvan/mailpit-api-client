"""module containing everything related to messages"""
import typing
import dataclasses as dc
import dataclasses_json as dj
import requests as r
import mailpit.models as m


@dj.dataclass_json
@dc.dataclass(init=True)
class Message:
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
    bcc: list[m.Contact] = dc.field(
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


class API:
    """
    class representing the messages API endpoint
    """

    def __init__(self, mailpit_url: str, timeout: int = None):
        self.mailpit_url = mailpit_url
        self.endpoint = "api/v1/messages"
        self.timeout = timeout
        self.last_response = None

    def get(self, limit: int = 50, start: int = 0) -> Messages:
        """
        send a GET request in order to retrieve messages
        :param limit: limit the returned number of messages
        :param start: start at an offset from the beginning
        :return: the messages returned by mailpit converted into models
        """
        response = r.get(
            f"{self.mailpit_url}/{self.endpoint}",
            params={"limit": limit, "start": start},
            timeout=self.timeout,
        )
        response.raise_for_status()
        self.last_response = response
        response.raise_for_status()
        return Messages.from_json(response.text)

    def delete(self, ids: typing.List[int]):
        """
        send a DELETE request to delete messages
        :param ids: the IDs of the messages to delete;
                    NOTE: passing an empty list will delete *all* messages
        """
        response = r.delete(
            f"{self.mailpit_url}/{self.endpoint}",
            data={"ids": ids},
            timeout=self.timeout,
        )
        self.last_response = response
        response.raise_for_status()

    def put(self, ids: typing.List[int], key: str, value: str):
        """
        update existing messages;
        for example pass "Read" as key and True as value to mark messages read
        :param ids: the IDs of the messages to update
        :param key: the message's attribute to update
        :param value: the value to update the attribute with
        """
        response = r.put(
            f"{self.mailpit_url}/{self.endpoint}",
            data={"ids": ids, key: value},
            timeout=self.timeout,
        )
        self.last_response = response
        response.raise_for_status()
