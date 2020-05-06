from mailit.bin.handleemail import EmailHandler
import logging
from django.core.management.base import BaseCommand
import sys
from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
import traceback
from mailit.exceptions import CouldNotFindIdentifier, TemporaryFailure
from mailit.answer import OutboundMessageAnswer
logging.basicConfig(filename='mailing_logger.txt', level=logging.INFO)


class Command(BaseCommand):
    args = ''
    help = 'Handles incoming EmailAnswer'

    def handle(self, *args, **options):
        lines = sys.stdin.readlines()
        if settings.INCOMING_EMAIL_LOGGING == 'ALL':
            if not settings.ADMINS:
                return
            text_content = "New incomming email"
            subject = "New incomming email"

            mail = EmailMultiAlternatives('%s%s' % (settings.EMAIL_SUBJECT_PREFIX, subject),
                text_content,  # content
                settings.DEFAULT_FROM_EMAIL,  # From
                [a[1] for a in settings.ADMINS]  # To
                )
            mail.attach('mail.txt', ''.join(lines), 'text/plain')
            mail.send()

        handler = EmailHandler(answer_class=OutboundMessageAnswer)
        try:
            answer = handler.handle(lines)
            answer.send_back()
        except CouldNotFindIdentifier:
            pass
        except TemporaryFailure:
            pass
        except:
            tb = traceback.format_exc()
            text_content = "Error the traceback was:\n" + tb
            #mail_admins('Error handling incoming email', html_message, html_message=html_message)
            subject = "Error handling incoming email"
            mail = EmailMultiAlternatives('%s%s' % (settings.EMAIL_SUBJECT_PREFIX, subject),
                text_content,  # content
                settings.DEFAULT_FROM_EMAIL,  # From
                [a[1] for a in settings.ADMINS],  # To
                )
            mail.attach('mail.txt', ''.join(lines), 'text/plain')
            mail.send()
