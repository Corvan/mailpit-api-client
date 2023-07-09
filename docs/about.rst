=====
About
=====

:Authors:
    Lars Liedtke <lars@familie-liedtke.net>
:Version:
    0.12.1

For work, I thought about introducing integration testing.
We are working with `Odoo <https://github.com/odoo/odoo>`_  and I wanted to test if e-mails created by Odoo really were sent.
I remembered `mailhog <https://github.com/mailhog/MailHog>`_, which I discovered to be abandoned.
Searching for an alternative, I found Mailpit - for which I decided to write an API-client in my free time.

-------
Mailpit
-------
Mailpit is software written Go, intended to be a testing tool for E-Mail.
It acts as a receiving E-Mail server and offers a Web Frontend as well as an API.
With it you can configure the software you want to test to send its E-Mail Messages to Mailpit and check via the frontend or the API if your software sent mail, correctly sent it, and using the frontend, how mail will be rendered.
If you want to learn more about Mailpit, have a look at its `README <https://github.com/axllent/mailpit#readme>`_ and at its `Wiki <https://github.com/axllent/mailpit/wiki>`_

----------
API-Client
----------
This API-Client uses Mailpit's API in order to provide classes and methods in Python, which are providing access to the API endpoints and the information returned of messages stored in Mailpit.
More information can be found in :doc:`usage`.

Additionally there are ``unittest`` Test-Cases and ``pytest`` Fixtures, which can be used to write (integration-) tests.
These helpers can be used to e.g. trigger sending an E-Mail message in a test and then
to check, if the message has been received by Mailpit. If it has not been received by mailpit your test will fail.
More information can be found in :doc:`testing/testing`.