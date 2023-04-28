import datetime

import httpx
import pytest
import respx

import mailpit.client.api as _c_api
import mailpit.client.message as _c_message
import mailpit.client.models as _c_models


class TestMessageModel:

    @pytest.fixture(scope="class")
    def response(self) -> str:
        yield """{
        "ID": "d7a5543b-96dd-478b-9b60-2b465c9884de",
        "Read": true,
        "From": {"Name": "John Doe", "Address": "john@example.com"},
        "To": [{"Name": "Jane Smith", "Address": "jane@example.com"}],
        "Cc": [],
        "Bcc": [],
        "Subject": "Message subject",
        "Date": "2016-09-07T16:46:00+13:00",
        "Text": "Plain text MIME part of the email",
        "HTML": "HTML MIME part (if exists)",
        "Size": 79499,
        "Inline": [
            {
                "PartID": "1.2",
                "FileName": "filename.gif",
                "ContentType": "image/gif",
                "ContentID": "919564503@07092006-1525",
                "Size": 7760
            }
        ],
        "Attachments": [
            {
                "PartID": "2",
                "FileName": "filename.doc",
                "ContentType": "application/msword",
                "ContentID": "",
                "Size": 43520
            }
        ]
    }"""

    def test_message(self, response):
        assert _c_message.Message.from_json(response) == _c_message.Message(
            id="d7a5543b-96dd-478b-9b60-2b465c9884de",
            read=True,
            subject="Message subject",
            date=datetime.datetime(
                year=2016,
                month=9,
                day=7,
                hour=16,
                minute=46,
                second=00,
                tzinfo=datetime.timezone(
                    datetime.timedelta(
                        hours=13
                    )
                )
            ),
            text="Plain text MIME part of the email",
            html="HTML MIME part (if exists)",
            size=79499,
            from_=_c_models.Contact(
                name="John Doe",
                address="john@example.com"
            ),
            to=[
                _c_models.Contact(
                    name="Jane Smith",
                    address="jane@example.com"
                )
            ],
            cc=[],
            bcc=[],
            inline=[
                _c_message.Attachment(
                    part_id='1.2',
                    file_name='filename.gif',
                    content_type='image/gif',
                    content_id='919564503@07092006-1525',
                    size=7760
                )
            ],
            attachments=[
                _c_message.Attachment(
                    part_id='2',
                    file_name='filename.doc',
                    content_type='application/msword',
                    content_id='',
                    size=43520
                )
            ]
        )


@pytest.fixture
def api() -> _c_api.API:
    yield _c_api.API("https://example.com")


class TestMessageAPI:
    @pytest.fixture(scope="class")
    def response(self):
        yield {
            "ID": "d7a5543b-96dd-478b-9b60-2b465c9884de",
            "Read": True,
            "From": {"Name": "John Doe", "Address": "john@example.com"},
            "To": [{"Name": "Jane Smith", "Address": "jane@example.com"}],
            "Cc": [],
            "Bcc": [],
            "Subject": "Message subject",
            "Date": "2016-09-07T16:46:00+13:00",
            "Text": "Plain text MIME part of the email",
            "HTML": "HTML MIME part (if exists)",
            "Size": 79499,
            "Inline": [
                {
                    "PartID": "1.2",
                    "FileName": "filename.gif",
                    "ContentType": "image/gif",
                    "ContentID": "919564503@07092006-1525",
                    "Size": 7760,
                }
            ],
            "Attachments": [
                {
                    "PartID": "2",
                    "FileName": "filename.doc",
                    "ContentType": "application/msword",
                    "ContentID": "",
                    "Size": 43520,
                }
            ],
        }

    @respx.mock
    def test_message_get(self, response, api):
        route = respx.get(
            "https://example.com/api/v1/message/d7a5543b-96dd-478b-9b60-2b465c9884de",
        )
        route.mock(return_value=httpx.Response(200, json=response))

        message = api.get_message("d7a5543b-96dd-478b-9b60-2b465c9884de")

        assert isinstance(message, _c_message.Message)
        assert api.last_response.status_code == 200


class TestAttachmentAPI:

    @respx.mock
    def test_attachment_get(self, api):
        route = respx.get(
            "https://example.com/api/v1/message/"
            "d7a5543b-96dd-478b-9b60-2b465c9884de/part/2"
        )
        route.mock(return_value=httpx.Response(200, text="Test"))

        attachment = api.get_message_attachment(
            "d7a5543b-96dd-478b-9b60-2b465c9884de", "2"
        )

        assert attachment == "Test"


class TestHeadersAPI:

    @pytest.fixture(scope="class")
    def response(self):
        yield {
            "Content-Type": [
                'multipart/related; type="multipart/alternative"; '
                'boundary="----=_NextPart_000_0013_01C6A60C.47EEAB80"'
            ],
            "Date": ["Wed, 12 Jul 2006 23:38:30 +1200"],
            "Delivered-To": ["user@example.com", "user-alias@example.com"],
            "From": ['"User Name" \\u003remote@example.com\\u003e'],
            "Message-Id": ["\\u003c001701c6a5a7$b3205580$0201010a@HomeOfficeSM\\u003e"],
        }

    @pytest.fixture(scope="class")
    def response_additional(self):
        yield {
            "Delivered-To": ["recipient@example.com"],
            "Received": [
                """by 2002:a0c:fe87:0:0:0:0:0 with SMTP id d7csp146390qvs;
        Tue, 26 Jul 2022 20:45:20 -0700 (PDT)""",
                """from mail-sor-f41.google.com (mail-sor-f41.google.com. [209.85.220.41])
        by mx.google.com with SMTPS id t3-20020a17090a2f8300b001f25e258dfasor335081pjd.34.2022.07.26.20.45.07
        for <recipient@example.com>
        (Google Transport Security);
        Tue, 26 Jul 2022 20:45:07 -0700 (PDT)""",
            ],
            "X-Received": [
                """by 2002:a17:90a:1943:b0:1ef:8146:f32f with SMTP id 3-20020a17090a194300b001ef8146f32fmr2327371pjh.112.1658893508159;
        Tue, 26 Jul 2022 20:45:08 -0700 (PDT)""",
                """by 2002:a17:90a:5e0b:b0:1f0:5565:ee6e with SMTP id w11-20020a17090a5e0b00b001f05565ee6emr2290528pjf.128.1658893506447;""",
            ],
            "ARC-Seal": [
                """i=1; a=rsa-sha256; t=1658893507; cv=none;
        d=google.com; s=arc-20160816;
        b=KrXcumoy4Oldq3Ny6ZLUfED4+/+4ndNbrM3uw1COEhqCVWWv7lLfFeNHTyxJQJLBK3
         tVgmPBX2XRmX+531CFRNquUDrqhsvc4kgIq0ExWPz99wG2vgsKWQ2x89AIfQ8sEYMwxY
         HOwErTH6XQuJ45YE+5Lt4pjMP+7NqnJ1NTRQyc7FB/c1Wt1JdTWscgaJGqUMnIFSbCPG
         xi0xpJnrIkh4giARIhabCRmVoo1g8BfzYrmy8uHtbIcDDuCJ8tN2lMLscwfw3u8hZWm6
         e1nAx4iDYyShdMZPPoUVoMHDf9P39DKwhdfb/xP/cQ6ulv7ECzVSp5DM8aLpfjw6SU9G
         JYJA=="""
            ],
            "ARC-Message-Signature": [
                """i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20160816;
        h=content-disposition:mime-version:message-id:subject:to:from:date
         :dkim-signature;
        bh=8shE8duj4atyKhQhO1qlS4/NgHN4ubjWq86U+mmAH9M=;
        b=TGK9vlNQRpyHvcpQonLjrFuLubL2mo9vT15CPwtC6ltsrYccKUozKiyb+id79dPatM
         y2unMpJqJFB4rZnASRm20Ck9dFRulM8bowO4l9BWKAUti9+u7bmLYbOPQCgDmJRA88ij
         YTkSKE8TuFMZQMJTkyZZTwE3F/Vrv84fAekWzGlwFoV3D6r6t1D5EUYUoR4xCVZdpMo1
         Ic0bEqgmRXl44uEqyVNpIC0w86Hzz84zl2V+nca+gxfObMzbJheDkOwVKkNNmr0ja936
         QZK+aO9s9VQGtqmjWtWhc1OWO50Bc5vE/krLFvZM6+vbMBEuDE5rkfHdf5mSD9Ix4xWl
         6/Rg=="""
            ],
            "ARC-Authentication-Results": [
                """i=1; mx.google.com;
       dkim=pass header.i=@gmail.com header.s=20210112 header.b=fpxRepVP;
       spf=pass (google.com: domain of sender@example.com designates 209.85.220.41 as permitted sender) smtp.mailfrom=sender@example.com;
       dmarc=pass (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com"""
            ],
            "Return-Path": ["""<sender@example.com>"""],
            "Received-SPF": [
                "pass (google.com: domain of sender@example.com designates "
                "209.85.220.41 as permitted sender) client-ip=209.85.220.41;"
            ],
            "Authentication-Results": [
                """ mx.google.com;
       dkim=pass header.i=@gmail.com header.s=20210112 header.b=fpxRepVP;
       spf=pass (google.com: domain of sender@example.com designates 209.85.220.41 as permitted sender) smtp.mailfrom=sender@example.com;
       dmarc=pass (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com"""
            ],
            "DKIM-Signature": [
                """v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=gmail.com; s=20210112;
        h=date:from:to:subject:message-id:mime-version:content-disposition;
        bh=8shE8duj4atyKhQhO1qlS4/NgHN4ubjWq86U+mmAH9M=;
        b=fpxRepVPdRgZF9VI4rCzO4n1l9+OHrm254/c1PaNcNnC1+0Rr78o1ASLvDKoQY4INc
         gRN1kJIk+ozQumJSfQPEIe+rHbJxe+wzjbYhEfUwBUnFHZykqvYWl6Xmjwg61IhxwwWk
         b3Gp/ODHkdQrm5QqIFACEn1fQmqkk4XBlcKMYEU/NOswGDOFULfbrhDcBWmR/gp2kHmT
         DkqRA9UJ1Cc6GO9lG+McRi8uLNaTymuLwzBydVV0bZOQTLxHQcQBTfUFrp/fwjHc9V19
         l9uQcn5rOOsh3vR37NGpv8WPi7BORLRFGjMVD0DZ7CtJwTDHz4EVvdLijt6YbUV9ecp1
         df3Q=="""
            ],
            "X-Google-DKIM-Signature": [
                """v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=1e100.net; s=20210112;
        h=x-gm-message-state:date:from:to:subject:message-id:mime-version
         :content-disposition;
        bh=8shE8duj4atyKhQhO1qlS4/NgHN4ubjWq86U+mmAH9M=;
        b=Z8ndxERf1NU67swjZ7cSjkSTTaa2YzhtrRyJkg0vnRxi87af7ECZNT+Zaxuxmxmqvb
         5T3IN2ymjPu1Y52EqRdZQpnzS/E5OjHbA6AYSn5qneNXNDxqJwp5qVSXuyB265QOo/9M
         bGp4fqfi8Qe5pmgkzyTqyrigWFOzcl23sCGXqvnrD8+0e+/n1dqo2tYk4v2KpSoAUxF0
         SNwHocpTDBDxOMEulUkQpqNlyZsgqNGdRhZmUN+2tQnpCQULd4B7+pydyWBCp9o8J1W4
         0IqmhJiNT8pB8MVzyUsWNG+WX9GBh8PK6XndOjmp2WvYh0LcUKeEYQ6zBsIdDFNEkMD1
         dU9w=="""
            ],
            "X-Gm-Message-State": [
                """AJIora+ZXWhiNwKn6ik6LuIUHc1hskP3Nneo2J0m0wSC9wwGXI1RPi1a
        Ml5Ex/pAryQwTi7MXqbUQkCIrEe5kU0="""
            ],
            "X-Google-Smtp-Source": [
                """AGRyM1v7CWOR6/X4d18Wv11XTnkfT25QfmsqBowwGsebQlPqhR1ogD3bo1sZRs/OSAHP7AjywIebfw=="""
            ],
            "Date": ["Wed, 27 Jul 2022 15:44:41 +1200"],
            "From": ["Sender Smith <sender@example.com>"],
            "To": ["Recipient Ross <recipient@example.com>"],
            "Subject": ["Plain text message"],
            "Message-Id": ["<20220727034441.7za34h6ljuzfpmj6@localhost.localhost>"],
            "MIME-Version": ["1.0"],
            "Content-Type": ["text/plain; charset=us-ascii"],
            "Content-Disposition": ["inline"],
        }

    @respx.mock
    def test_header_get(self, api, response):
        route = respx.get(
            "https://example.com/api/v1/message/"
            "d7a5543b-96dd-478b-9b60-2b465c9884de/headers"
        )

        route.mock(return_value=httpx.Response(200, json=response))

        headers = api.get_message_headers("d7a5543b-96dd-478b-9b60-2b465c9884de")

        assert headers.content_type[0] == (
                   'multipart/related; type="multipart/alternative"; '
                   'boundary="----=_NextPart_000_0013_01C6A60C.47EEAB80"'
               )
        assert headers.date[0] == datetime.datetime(
            2006, 7, 12, 23, 38, 30,
            tzinfo=datetime.timezone(datetime.timedelta(seconds=43200))
        )
        assert headers.delivered_to == ["user@example.com", "user-alias@example.com"]
        assert headers.from_[0] == '"User Name" \\u003remote@example.com\\u003e'
        assert (
                headers.message_id[0] == "\\u003c001701c6a5a7$b3205580$0201010a@HomeOfficeSM\\u003e"
        )

    @respx.mock
    def test_header_additional(self, api, response_additional):
        route = respx.get(
            "https://example.com/api/v1/message/"
            "<20220727034441.7za34h6ljuzfpmj6@localhost.localhost>/headers"
        )
        route.mock(return_value=httpx.Response(200, json=response_additional))

        headers = api.get_message_headers(
            "<20220727034441.7za34h6ljuzfpmj6@localhost.localhost>"
        )
        assert isinstance(headers, _c_message.Headers)
        assert headers.from_[0] == "Sender Smith <sender@example.com>"
        assert headers.additional["Received"][1] == """from mail-sor-f41.google.com (mail-sor-f41.google.com. [209.85.220.41])
        by mx.google.com with SMTPS id t3-20020a17090a2f8300b001f25e258dfasor335081pjd.34.2022.07.26.20.45.07
        for <recipient@example.com>
        (Google Transport Security);
        Tue, 26 Jul 2022 20:45:07 -0700 (PDT)"""
