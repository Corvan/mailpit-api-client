"""module containing API related"""
import logging
from typing import Optional, List, Any

import httpx

import mailpit.client.models as models

_log = logging.getLogger("mailpit_client")


class API:
    """
    class representing the different endpoints of the API
    """

    # pylint: disable=too-few-public-methods

    MESSAGES_ENDPOINT = "api/v1/messages"
    MESSAGE_ENDPOINT = "api/v1/message"

    def __init__(self, mailpit_url: str, timeout: Optional[int] = None):
        self.mailpit_url = mailpit_url
        self.timeout = timeout
        self.last_response: Optional[httpx.Response] = None

    def get_messages(self, limit: int = 50, start: int = 0) -> models.Messages:
        """
        send a GET request in order to retrieve messages

        :param limit: limit the returned number of messages
        :param start: start at an offset from the beginning
        :return: the messages returned by mailpit converted into models
        """

        # pylint: disable = no-member

        response = httpx.get(
            f"{self.mailpit_url}/{API.MESSAGES_ENDPOINT}",
            params={"limit": limit, "start": start},
            timeout=self.timeout,
        )
        self.last_response = response
        response.raise_for_status()
        _log.debug(response.text)
        return models.Messages.from_json(response.text)  # type: ignore

    def delete_messages(self, ids: List[str]):
        """
        send a DELETE request to delete messages

        :param ids: the IDs of the messages to delete;
                    NOTE: passing an empty list will delete *all* messages
        """
        response = httpx.request(
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
        response = httpx.put(
            f"{self.mailpit_url}/{API.MESSAGES_ENDPOINT}",
            data={"ids": ids, key: value},
            timeout=self.timeout,
        )
        self.last_response = response
        response.raise_for_status()

    def get_message(self, message_id: str) -> models.Message:
        """
        Send a GET request to get a certain Message by its Message-ID

        :param message_id: The Message-ID to get the message by
        """

        # pylint: disable = no-member

        response = httpx.get(
            f"{self.mailpit_url}/{API.MESSAGE_ENDPOINT}/{message_id}",
            timeout=self.timeout,
        )
        self.last_response = response
        response.raise_for_status()
        _log.debug(response.text)
        message = models.Message.from_json(response.text)
        return message

    def get_message_attachment(self, message_id: str, part_id: str) -> str:
        """
        Send a GET request to the message endpoint with querying for the part_id
        of an attachment

        :param message_id: the Message-ID the attachment belongs to
        :param part_id: the Part-ID of the attachment to receive
        :return the attachment's data
        """
        response = httpx.get(
            f"{self.mailpit_url}/{API.MESSAGE_ENDPOINT}/{message_id}/part/{part_id}",
            timeout=self.timeout,
        )
        self.last_response = response
        response.raise_for_status()
        return response.text

    def get_message_headers(self, message_id: str) -> models.Headers:
        """
        Send a GET request to get a message's Headers

        :param message_id: The Message-ID to get the headers for
        """
        response = httpx.get(
            f"{self.mailpit_url}/{API.MESSAGE_ENDPOINT}/{message_id}/headers",
            timeout=self.timeout,
        )
        self.last_response = response
        response.raise_for_status()
        return models.Headers.from_json(response.text)  # type: ignore
