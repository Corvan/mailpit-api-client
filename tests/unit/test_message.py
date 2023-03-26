import unittest

import httpx
import respx

import mailpit.api
import mailpit.message as m
import mailpit.models


class MessageModelTestCase(unittest.TestCase):
    RESPONSE = """{
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

    message: m.Message = m.Message.from_json(RESPONSE)

    def test_message(self):
        self.assertIsInstance(MessageModelTestCase.message, m.Message)
        self.assertEqual("d7a5543b-96dd-478b-9b60-2b465c9884de", self.message.id)
        self.assertEqual(True, MessageModelTestCase.message.read)
        self.assertEqual("Message subject", self.message.subject)
        self.assertEqual("2016-09-07T16:46:00+13:00", self.message.date)
        self.assertEqual("Plain text MIME part of the email", self.message.text)
        self.assertEqual("HTML MIME part (if exists)", self.message.html)
        self.assertEqual(79499, self.message.size)

    def test_message_from(self):
        self.assertIsInstance(self.message.from_, mailpit.models.Contact)
        self.assertEqual("John Doe", self.message.from_.name)
        self.assertEqual("john@example.com", self.message.from_.address)

    def test_message_to(self):
        self.assertEqual(1, len(self.message.to))
        self.assertIsInstance(self.message.to[0], mailpit.models.Contact)
        self.assertEqual("Jane Smith", self.message.to[0].name)
        self.assertEqual("jane@example.com", self.message.to[0].address)

    def test_message_cc(self):
        self.assertEqual([], self.message.cc)

    def test_message_bcc(self):
        self.assertEqual([], self.message.bcc)


class MessageAPITestCase(unittest.TestCase):
    RESPONSE = {
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

    def setUp(self) -> None:
        self.api = mailpit.api.API("https://example.com")

    @respx.mock
    def test_message_get(self):
        route = respx.get(
            "https://example.com/api/v1/message/d7a5543b-96dd-478b-9b60-2b465c9884de",
        )
        route.mock(return_value=httpx.Response(200, json=MessageAPITestCase.RESPONSE))

        message = self.api.get_message("d7a5543b-96dd-478b-9b60-2b465c9884de")

        self.assertIsInstance(message, m.Message)
        self.assertEqual(200, self.api.last_response.status_code)


class AttachmentAPITestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.api = mailpit.api.API("https://example.com")

    @respx.mock
    def test_attachment_get(self):
        route = respx.get(
            "https://example.com/api/v1/message/"
            "d7a5543b-96dd-478b-9b60-2b465c9884de/part/2"
        )
        route.mock(return_value=httpx.Response(200, text="Test"))

        attachment = self.api.get_message_attachment(
            "d7a5543b-96dd-478b-9b60-2b465c9884de", "2"
        )

        self.assertEqual("Test", attachment)


class HeadersAPITestCase(unittest.TestCase):
    RESPONSE = {
        "Content-Type": [
            'multipart/related; type="multipart/alternative"; '
            'boundary="----=_NextPart_000_0013_01C6A60C.47EEAB80"'
        ],
        "Date": ["Wed, 12 Jul 2006 23:38:30 +1200"],
        "Delivered-To": ["user@example.com", "user-alias@example.com"],
        "From": ['"User Name" \\u003remote@example.com\\u003e'],
        "Message-Id": ["\\u003c001701c6a5a7$b3205580$0201010a@HomeOfficeSM\\u003e"],
    }
    RESPONSE_ADDITIONAL = {
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

    def setUp(self) -> None:
        self.api = mailpit.api.API("https://example.com")

    @respx.mock
    def test_header_get(self):
        route = respx.get(
            "https://example.com/api/v1/message/"
            "d7a5543b-96dd-478b-9b60-2b465c9884de/headers"
        )

        route.mock(return_value=httpx.Response(200, json=self.RESPONSE))

        headers = self.api.get_message_headers("d7a5543b-96dd-478b-9b60-2b465c9884de")

        self.assertEqual(
            (
                'multipart/related; type="multipart/alternative"; '
                'boundary="----=_NextPart_000_0013_01C6A60C.47EEAB80"'
            ),
            headers.content_type[0],
        )
        self.assertEqual("Wed, 12 Jul 2006 23:38:30 +1200", headers.date[0])
        self.assertEqual(
            ["user@example.com", "user-alias@example.com"], headers.delivered_to
        )
        self.assertEqual(
            '"User Name" \\u003remote@example.com\\u003e', headers.from_[0]
        )
        self.assertEqual(
            "\\u003c001701c6a5a7$b3205580$0201010a@HomeOfficeSM\\u003e",
            headers.message_id[0],
        )

    @respx.mock
    def test_header_additional(self):
        route = respx.get(
            "https://example.com/api/v1/message/"
            "<20220727034441.7za34h6ljuzfpmj6@localhost.localhost>/headers"
        )
        route.mock(return_value=httpx.Response(200, json=self.RESPONSE_ADDITIONAL))

        headers = self.api.get_message_headers(
            "<20220727034441.7za34h6ljuzfpmj6@localhost.localhost>"
        )
        self.assertIsInstance(headers, m.Headers)
        self.assertEqual("Sender Smith <sender@example.com>", headers.from_[0])
        self.assertEqual(
            """from mail-sor-f41.google.com (mail-sor-f41.google.com. [209.85.220.41])
        by mx.google.com with SMTPS id t3-20020a17090a2f8300b001f25e258dfasor335081pjd.34.2022.07.26.20.45.07
        for <recipient@example.com>
        (Google Transport Security);
        Tue, 26 Jul 2022 20:45:07 -0700 (PDT)""",
            headers.additional["Received"][1],
        )
