import datetime as _dt


class TestMessageApiGet:
    def test_get_message__subject(self, sent_message):
        assert sent_message.subject == "Plain text message"

    def test_get_message__size(self, sent_message):
        assert 7917 <= sent_message.size <= 7927

    def test_get_message__attachment(self, sent_message):
        assert len(sent_message.attachments) == 0

    def test_get_message_from__name(self, sent_message):
        assert sent_message.from_.name == "Sender Smith"

    def test_get_message_from__address(self, sent_message):
        assert sent_message.from_.address == "sender@example.com"

    def test_get_message_to__count(self, sent_message):
        assert len(sent_message.to) == 1

    def test_get_message_to__name(self, sent_message):
        assert sent_message.to[0].name == "Recipient Ross"

    def test_get_message_to__address(self, sent_message):
        assert sent_message.to[0].address == "recipient@example.com"

    def test_get_message_cc__count(self, sent_message):
        assert len(sent_message.cc) == 0

    def test_get_message_bcc__count(self, sent_message):
        assert len(sent_message.bcc) == 0

    def test_get_message__date(self, sent_message):
        assert sent_message.date == _dt.datetime.fromisoformat(
            "2022-07-27 15:44:41.000000+12:00"
        )

    def test_get_message__read(self, sent_message):
        assert sent_message.read is True

    def test_get_message_inline(self, sent_message):
        assert len(sent_message.inline) == 0

    def test_get_message_text(self, sent_message):
        assert (
            sent_message.text
            == "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
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

    def test_get_message_html(self, sent_message):
        assert sent_message.html == ""


class TestMessageDelete:
    ...


class TestMessagePut:
    ...
