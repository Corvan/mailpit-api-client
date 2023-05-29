"""module containing API related"""
import logging as _logging
from typing import Optional, List, Any

import httpx as _httpx

import mailpit.client.models as _models

_log = _logging.getLogger("mailpit_client")


class API:
    """
    class representing the message-endpoint of the API
    """

    # pylint: disable=too-few-public-methods

    MESSAGES_ENDPOINT = "api/v1/messages"
    MESSAGE_ENDPOINT = "api/v1/message"

    def __init__(self, mailpit_url: str, timeout: Optional[int] = None):
        self.mailpit_url = mailpit_url
        self.timeout = timeout
        self.last_response: Optional[_httpx.Response] = None

    def get_messages(self, limit: int = 50, start: int = 0) -> _models.Messages:
        """
        send a GET request in order to retrieve messages

        :param limit: limit the returned number of messages
        :param start: start at an offset from the beginning
        :return: the messages returned by mailpit converted into models
        """

        # pylint: disable = no-member

        response = _httpx.get(
            f"{self.mailpit_url}/{API.MESSAGES_ENDPOINT}",
            params={"limit": limit, "start": start},
            timeout=self.timeout,
        )
        self.last_response = response
        response.raise_for_status()
        _log.debug(response.text)
        return _models.Messages.from_json(response.text)  # type: ignore

    def delete_messages(self, ids: List[str]):
        """
        send a DELETE request to delete messages

        :param ids: the IDs of the messages to delete;
                    NOTE: passing an empty list will delete *all* messages
        """
        response = _httpx.request(
            method="DELETE",
            url=f"{self.mailpit_url}/{API.MESSAGES_ENDPOINT}",
            data={"ids": ids},
            timeout=self.timeout,
        )
        self.last_response = response
        response.raise_for_status()

    def put_messages(self, ids: List[str], key: str, value: Any):
        """
        update existing messages;
        for example pass "Read" as key and True as value to mark messages read

        :param ids: the IDs of the messages to update
        :param key: the message's attribute to update
        :param value: the value to update the attribute with
        """
        response = _httpx.put(
            f"{self.mailpit_url}/{API.MESSAGES_ENDPOINT}",
            data={"ids": ids, key: value},
            timeout=self.timeout,
        )
        self.last_response = response
        response.raise_for_status()

    def get_message(self, message_id: str) -> _models.Message:
        """


        :param message_id:
        """

        # pylint: disable = no-member

        response = _httpx.get(
            f"{self.mailpit_url}/{API.MESSAGE_ENDPOINT}/{message_id}",
            timeout=self.timeout,
        )
        self.last_response = response
        response.raise_for_status()
        _log.debug(response.text)
        message = _models.Message.from_json(response.text)
        return message

    def get_message_attachment(self, message_id: str, part_id: str):
        """


        :param message_id:
        :param part_id:
        """
        response = _httpx.get(
            f"{self.mailpit_url}/{API.MESSAGE_ENDPOINT}/{message_id}/part/{part_id}",
            timeout=self.timeout,
        )
        self.last_response = response
        response.raise_for_status()
        return response.text

    def get_message_headers(self, message_id: str):
        """


        :param message_id:
        """
        response = _httpx.get(
            f"{self.mailpit_url}/{API.MESSAGE_ENDPOINT}/{message_id}/headers",
            timeout=self.timeout,
        )
        self.last_response = response
        response.raise_for_status()
        return _models.Headers.from_json(response.text)  # type: ignore
