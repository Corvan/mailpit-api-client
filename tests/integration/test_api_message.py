import datetime as _dt
import pytest as _pt

import mailpit.client.api as _api
import mailpit.client.models.message as _m


# noinspection PyShadowingNames
class TestMessageApiGet:
    def test_get_message(self, sent_message_id_without_attachment: str, api: _api.API):
        message = api.get_message(sent_message_id_without_attachment)
        assert message.subject == "Plain text message"
        assert (
            message.message_id == "20220727034441.7za34h6ljuzfpmj6@localhost.localhost"
        )
        assert 7900 <= message.size <= 7945
        assert len(message.attachments) == 0
        assert message.from_.name == "Sender Smith"
        assert message.from_.address == "sender@example.com"
        assert len(message.to) == 1
        assert message.to[0].name == "Recipient Ross"
        assert message.to[0].address == "recipient@example.com"
        assert len(message.cc) == 0
        assert len(message.bcc) == 0
        assert message.date == _dt.datetime.fromisoformat(
            "2022-07-27 15:44:41.000000+12:00"
        )
        assert message.read is True
        assert len(message.inline) == 0
        assert (
            message.text == "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
            "Cras non massa lacinia, \r\n"
            "fringilla ex vel, ornare nulla. Suspendisse "
            "dapibus commodo sapien, non \r\n"
            "hendrerit diam feugiat sit amet. Nulla lorem "
            "quam, laoreet vitae nisl volutpat, \r\n"
            "mollis bibendum felis. In eget ultricies justo. "
            "Donec vitae hendrerit tortor, at \r\n"
            "posuere libero. Fusce a gravida nibh. Nulla ac odio ex.\r\n"
            "\r\n"
            "Aliquam sem turpis, cursus vitae condimentum "
            "at, scelerisque pulvinar lectus. \r\n"
            "Cras tempor nisl ut arcu interdum, et luctus "
            "arcu cursus. Maecenas mollis \r\n"
            "sagittis commodo. Mauris ac lorem nec ex "
            "interdum consequat. Morbi congue \r\n"
            "ultrices ullamcorper. Aenean ex tortor, "
            "dapibus quis dapibus iaculis, iaculis \r\n"
            "eget felis. Vestibulum purus ante, "
            "efficitur in turpis ac, tristique laoreet \r\n"
            "orci. Nulla facilisi. Praesent "
            "mollis orci posuere elementum laoreet. \r\n"
            "Pellentesque enim nibh, varius at "
            "ante id, consequat posuere ante.\r\n"
            "\r\n"
            "Cras maximus venenatis nulla nec cursus."
            " Morbi convallis, enim eget viverra \r\n"
            "vulputate, ipsum arcu tincidunt tortor, "
            "ut cursus dui enim commodo quam. Donec \r\n"
            "et vulputate quam. Vivamus non posuere erat. Nam commodo pellentesque \r\n"
            "condimentum. Vivamus condimentum eros "
            "at odio dictum feugiat. Ut imperdiet \r\n"
            "tempor luctus. Aenean varius libero "
            "ac faucibus dictum. Aliquam sed finibus \r\n"
            "massa. Morbi dolor lorem, feugiat "
            "quis neque et, suscipit posuere ex. Sed auctor \r\n"
            "et augue at finibus. Vestibulum "
            "interdum mi ac justo porta aliquam. Curabitur \r\n"
            "nec enim sit amet enim aliquet "
            "accumsan. Etiam accumsan tellus tortor, interdum \r\n"
            "sodales odio finibus eu. Integer "
            "eget ante eu nisi lobortis pulvinar et vel \r\n"
            "ipsum. Cras condimentum posuere vulputate.\r\n"
            "\r\n"
            "Cras nulla felis, blandit vitae egestas "
            "quis, fringilla ut dolor. Phasellus est \r\n"
            "augue, feugiat eu risus quis, posuere "
            "ultrices libero. Phasellus non nunc eget \r\n"
            "justo sollicitudin tincidunt. Praesent "
            "pretium dui id felis bibendum sodales. \r\n"
            "Phasellus eget dictum libero, auctor "
            "tempor nibh. Suspendisse posuere libero \r\n"
            "venenatis elit imperdiet porttitor. "
            "In condimentum dictum luctus. Nullam in \r\n"
            "nulla vitae augue blandit posuere. "
            "Vestibulum consectetur ultricies tincidunt. \r\n"
            "Vivamus dolor quam, pharetra sed eros "
            "sed, hendrerit ultrices diam. Vestibulum \r\n"
            "vulputate tellus eget tellus lacinia,"
            " a pulvinar velit vulputate. Suspendisse \r\n"
            "mauris odio, scelerisque eget turpis sed, "
            "tincidunt ultrices magna. Nunc arcu \r\n"
            "arcu, commodo et porttitor quis, accumsan "
            "viverra purus. Fusce id libero iaculis \r\n"
            "lorem tristique commodo porttitor id ipsum. "
            "Vestibulum odio dui, tincidunt eget \r\n"
            "lectus vel, tristique lacinia libero. "
            "Aliquam dapibus ac felis vitae cursus.\r\n"
        )
        assert message.html == ""


class TestMessageApiDelete:
    ...


class TestMessageApiPut:
    ...


# noinspection PyShadowingNames
class TestMessageApiAttachments:
    def test_get_message_without_attachment(
        self, sent_message_id_without_attachment: str, api: _api.API
    ):
        message = api.get_message(sent_message_id_without_attachment)
        assert len(message.attachments) == 0
        assert len(message.inline) == 0

    def test_get_message_with_attachment(
        self, sent_message_id_with_attachment: str, api: _api.API
    ):
        ...


# noinspection PyShadowingNames
class TestMessageApiHeaders:
    def test_get_headers(self, sent_message_id_without_attachment: str, api: _api.API):
        headers = api.get_message_headers(sent_message_id_without_attachment)
        assert headers.content_type[0] == "text/plain; charset=us-ascii"
        assert headers.date[0] == _dt.datetime(
            2022, 7, 27, 15, 44, 41, tzinfo=_dt.timezone(_dt.timedelta(seconds=43200))
        )
        assert headers.delivered_to[0] == "recipient@example.com"
        assert headers.from_[0] == "Sender Smith <sender@example.com>"
        assert (
            headers.message_id[0]
            == "<20220727034441.7za34h6ljuzfpmj6@localhost.localhost>"
        )
        del headers.additional["Received"]  # Not predictable, bc current time
        # and hostnames included
        assert headers.additional == {
            "Arc-Authentication-Results": [
                "i=1; mx.google.com; dkim=pass header.i=@gmail.com header.s=20210112 "
                "header.b=fpxRepVP; spf=pass (google.com: domain of sender@example.com "
                "designates 209.85.220.41 as permitted sender) "
                "smtp.mailfrom=sender@example.com; dmarc=pass "
                "(p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com"
            ],
            "Arc-Message-Signature": [
                "i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20160816; "
                "h=content-disposition:mime-version:message-id:subject:to:from:date "
                ":dkim-signature; bh=8shE8duj4atyKhQhO1qlS4/NgHN4ubjWq86U+mmAH9M=; "
                "b=TGK9vlNQRpyHvcpQonLjrFuLubL2mo9vT15CPwtC6ltsrYccKUozKiyb+id79dPatM "
                "y2unMpJqJFB4rZnASRm20Ck9dFRulM8bowO4l9BWKAUti9+u7bmLYbOPQCgDmJRA88ij "
                "YTkSKE8TuFMZQMJTkyZZTwE3F/Vrv84fAekWzGlwFoV3D6r6t1D5EUYUoR4xCVZdpMo1 "
                "Ic0bEqgmRXl44uEqyVNpIC0w86Hzz84zl2V+nca+gxfObMzbJheDkOwVKkNNmr0ja936 "
                "QZK+aO9s9VQGtqmjWtWhc1OWO50Bc5vE/krLFvZM6+vbMBEuDE5rkfHdf5mSD9Ix4xWl "
                "6/Rg=="
            ],
            "Arc-Seal": [
                "i=1; a=rsa-sha256; t=1658893507; cv=none; d=google.com; "
                "s=arc-20160816; b=KrXcumoy4Oldq3Ny6ZLUfED4+/+4ndNbrM3uw1COEhqCVWWv7lL"
                "fFeNHTyxJQJLBK3 tVgmPBX2XRmX+531CFRNquUDrqhsvc4kgIq0ExWPz99wG2vgsKWQ2x"
                "89AIfQ8sEYMwxY HOwErTH6XQuJ45YE+5Lt4pjMP+7NqnJ1NTRQyc7FB/c1Wt1JdTWscga"
                "JGqUMnIFSbCPG xi0xpJnrIkh4giARIhabCRmVoo1g8BfzYrmy8uHtbIcDDuCJ8tN2lML"
                "scwfw3u8hZWm6 e1nAx4iDYyShdMZPPoUVoMHDf9P39DKwhdfb/xP/cQ6ulv7ECzVSp5D"
                "M8aLpfjw6SU9G JYJA=="
            ],
            "Authentication-Results": [
                "mx.google.com; dkim=pass header.i=@gmail.com header.s=20210112 "
                "header.b=fpxRepVP; spf=pass (google.com: domain of sender@example.com "
                "designates 209.85.220.41 as permitted sender) smtp.mailfrom=sender@e"
                "xample.com; dmarc=pass (p=NONE sp=QUARANTINE dis=NONE) "
                "header.from=gmail.com"
            ],
            "Content-Disposition": ["inline"],
            "Dkim-Signature": [
                "v=1; a=rsa-sha256; c=relaxed/relaxed; d=gmail.com; s=20210112; "
                "h=date:from:to:subject:message-id:mime-version:content-disposition; "
                "bh=8shE8duj4atyKhQhO1qlS4/NgHN4ubjWq86U+mmAH9M=; "
                "b=fpxRepVPdRgZF9VI4rCzO4n1l9+OHrm254/c1PaNcNnC1+0Rr78o1ASLvDKoQY4INc "
                "gRN1kJIk+ozQumJSfQPEIe+rHbJxe+wzjbYhEfUwBUnFHZykqvYWl6Xmjwg61IhxwwWk "
                "b3Gp/ODHkdQrm5QqIFACEn1fQmqkk4XBlcKMYEU/NOswGDOFULfbrhDcBWmR/gp2kHmT "
                "DkqRA9UJ1Cc6GO9lG+McRi8uLNaTymuLwzBydVV0bZOQTLxHQcQBTfUFrp/fwjHc9V19 "
                "l9uQcn5rOOsh3vR37NGpv8WPi7BORLRFGjMVD0DZ7CtJwTDHz4EVvdLijt6YbUV9ecp1 "
                "df3Q=="
            ],
            "Mime-Version": ["1.0"],
            "Received-Spf": [
                "pass (google.com: domain of sender@example.com designates "
                "209.85.220.41 as permitted sender) client-ip=209.85.220.41;"
            ],
            "Return-Path": ["<sender@example.com>", "<sender@example.com>"],
            "Subject": ["Plain text message"],
            "To": ["Recipient Ross <recipient@example.com>"],
            "X-Gm-Message-State": [
                "AJIora+ZXWhiNwKn6ik6LuIUHc1hskP3Nneo2J0m0wSC9wwGXI1RPi1a "
                "Ml5Ex/pAryQwTi7MXqbUQkCIrEe5kU0="
            ],
            "X-Google-Dkim-Signature": [
                "v=1; a=rsa-sha256; c=relaxed/relaxed; d=1e100.net; "
                "s=20210112; h=x-gm-message-state:date:from:to:subject:"
                "message-id:mime-version :content-disposition; "
                "bh=8shE8duj4atyKhQhO1qlS4/NgHN4ubjWq86U+mmAH9M=; "
                "b=Z8ndxERf1NU67swjZ7cSjkSTTaa2YzhtrRyJkg0vnRxi87af7ECZNT+Zaxuxmxmqvb "
                "5T3IN2ymjPu1Y52EqRdZQpnzS/E5OjHbA6AYSn5qneNXNDxqJwp5qVSXuyB265QOo/9M "
                "bGp4fqfi8Qe5pmgkzyTqyrigWFOzcl23sCGXqvnrD8+0e+/n1dqo2tYk4v2KpSoAUxF0 "
                "SNwHocpTDBDxOMEulUkQpqNlyZsgqNGdRhZmUN+2tQnpCQULd4B7+pydyWBCp9o8J1W4 "
                "0IqmhJiNT8pB8MVzyUsWNG+WX9GBh8PK6XndOjmp2WvYh0LcUKeEYQ6zBsIdDFNEkMD1 "
                "dU9w=="
            ],
            "X-Google-Smtp-Source": [
                "AGRyM1v7CWOR6/X4d18Wv11XTnkfT25QfmsqBowwGsebQlPqhR1ogD3bo1sZRs/"
                "OSAHP7AjywIebfw=="
            ],
            "X-Received": [
                "by 2002:a17:90a:1943:b0:1ef:8146:f32f with SMTP id "
                "3-20020a17090a194300b001ef8146f32fmr2327371pjh.112.1658893508159; "
                "Tue, 26 Jul 2022 20:45:08 -0700 (PDT)",
                "by 2002:a17:90a:5e0b:b0:1f0:5565:ee6e with SMTP id "
                "w11-20020a17090a5e0b00b001f05565ee6emr2290528pjf.128.1658893506447; "
                "Tue, 26 Jul 2022 20:45:06 -0700 (PDT)",
            ],
        }
