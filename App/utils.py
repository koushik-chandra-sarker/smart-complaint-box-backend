import json
import random
import string
from io import BytesIO

from PIL import Image
from django.core import mail
from django.core.files import File
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend
from django.http import QueryDict
from django.utils.text import slugify
from rest_framework import parsers

from App.settings import SITE_URL
from author.models.mail_model import MailInfo
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_mail(body, name=None, mail_to=None):
    try:

        con = mail.get_connection()
        mail_setting = MailInfo.objects.get(active=True)
        host = mail_setting.host
        host_user = mail_setting.mail
        host_pass = mail_setting.password
        host_port = mail_setting.port
        mail_obj = EmailBackend(
            host=host,
            port=host_port,
            username=host_user,
            password=host_pass,
            use_tls=mail_setting.tls,
            use_ssl=mail_setting.ssl,
        )
        mail_obj.open()
        msg = mail.EmailMessage(
            f'title',
            f'Your Message',
            f'Your Mail',
            host_user,
            [mail_to],
            connection=con,
        )
        mail_obj.send_messages([msg])
        mail_obj.close()
        return True

    except Exception as _error:
        return False


def send_html_mail(to, url, contact_url, subject):
    try:
        html_message = render_to_string("email_template.html", {'url': SITE_URL + url, 'contact_url': contact_url})
        plain_message = strip_tags(html_message)
        con = mail.get_connection()
        mail_setting = MailInfo.objects.get(active=True)
        host = mail_setting.host
        host_user = mail_setting.mail
        host_pass = mail_setting.password
        host_port = mail_setting.port
        mail_obj = EmailBackend(
            host=host,
            port=host_port,
            username=host_user,
            password=host_pass,
            use_tls=mail_setting.tls,
            use_ssl=mail_setting.ssl,
        )
        mail_obj.open()
        email = mail.EmailMultiAlternatives(
            subject,
            plain_message,
            host_user,
            [to],
            connection=con,
        )
        email.attach_alternative(html_message, "text/html")
        mail_obj.send_messages([email])
    except Exception as _error:
        return False


class MultipartJsonParser(parsers.MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        )
        data = {}
        # find the data field and parse it
        data = json.loads(result.data["data"])
        qdict = QueryDict('', mutable=True)
        qdict.update(data)
        return parsers.DataAndFiles(qdict, result.files)
