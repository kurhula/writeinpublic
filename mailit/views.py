import logging

from django.views.generic.edit import UpdateView
from .models import MailItTemplate
from .forms import MailitTemplateForm
from subdomains.utils import reverse
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from instance.models import WriteItInstance
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from mailit.exceptions import CouldNotFindIdentifier, TemporaryFailure
from mailit.answer import OutboundMessageAnswer
from mailit.bin.handleemail import EmailHandler

logger = logging.getLogger(__name__)


class MailitTemplateUpdateView(UpdateView):
    model = MailItTemplate
    form_class = MailitTemplateForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MailitTemplateUpdateView, self).dispatch(*args, **kwargs)

    def get_object(self):
        self.writeitinstance = get_object_or_404(WriteItInstance, slug=self.request.subdomain)
        if not self.writeitinstance.owner.__eq__(self.request.user):
            raise Http404
        self.object = self.writeitinstance.mailit_template
        return self.object

    def get_form_kwargs(self):
        kwargs = super(MailitTemplateUpdateView, self).get_form_kwargs()
        self.object = self.get_object()
        kwargs['writeitinstance'] = self.object.writeitinstance
        return kwargs

    def get_success_url(self):
        return reverse('writeitinstance_template_update', subdomain=self.writeitinstance.slug)


class IncomingMail(View):
    """
    https://sendgrid.com/docs/API_Reference/Parse_Webhook/inbound_email.html
    """
    def get(self, request):
        logger.info("SendGrid Inbound mail webhook GET %r", request.GET)
        return HttpResponse()

    def post(self, request):
        handler = EmailHandler(answer_class=OutboundMessageAnswer)
        try:
            email = request.POST['email']
            logger.debug("SendGrid Inbound mail webhook POST email\n\n%s" % email)
            answer = handler.handle(email)
            answer.send_back()
        except CouldNotFindIdentifier as e:
            logger.warn(e)

        return HttpResponse()
