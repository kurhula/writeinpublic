from django.db.models import Count
from nuntium.user_section.views import WriteItInstanceDetailBaseView


class StatsPerInstance(object):
    def __init__(self, writeitinstance=None):
        self.writeitinstance = writeitinstance

    def get_stats(self):
        stats = [
            ('Confirmed public messages', self.public_confirmed_messages),
            ('Public messages with answers', self.public_messages_with_answers),
        ]
        private_message_count = self.amount_of_private_messages
        if private_message_count:
            stats.append(('Total private messages', private_message_count))
            stats.append(('Total public messages', self.amount_of_public_messages))
        stats.append(('Total messages', self.amount_of_messages))
        return stats

    @property
    def amount_of_messages(self):
        return self.writeitinstance.message_set.count()

    @property
    def amount_of_public_messages(self):
        return self.writeitinstance.message_set.filter(public=True).count()

    @property
    def amount_of_private_messages(self):
        private_message_count = self.writeitinstance.message_set.filter(public=False).count()
        if private_message_count:
            return private_message_count

    @property
    def public_messages_with_answers(self):
        return (self.writeitinstance.message_set
            .annotate(num_answers=Count('answers'))
            .filter(public=True, num_answers__gt=0)
            .count())

    @property
    def public_confirmed_messages(self):
        return self.writeitinstance.message_set.filter(public=True, confirmated=True).count()


class StatsView(WriteItInstanceDetailBaseView):
    template_name = 'nuntium/profiles/stats.html'

    def get_context_data(self, **kwargs):
        context = super(StatsView, self).get_context_data(**kwargs)
        context['stats'] = StatsPerInstance(writeitinstance=self.object)
        return context
