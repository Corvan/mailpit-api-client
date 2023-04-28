
class TestMessage:

    def test_get_message(self, log, smtp_server, message):
        log.info("testing get")

    def test_get_message_attachment(self, log, smtp_server, message):
        log.info("testing attachment")

    def test_get_message_headers(self, log, smtp_server, message):
        log.info("testing headers")
