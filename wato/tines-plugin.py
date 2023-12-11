#!/usr/bin/python3

# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_notification_parameters("tines-plugin.py", Dictionary(
    elements = [
        ("TinesWebhookUrl", TextAscii(
            title = _("Tines Webhook Url (mandatory)"),
            help = _("Tines Webhook Url - copy from a Tines webhook task"),
            allow_empty = False,
        )),
    ]
))
