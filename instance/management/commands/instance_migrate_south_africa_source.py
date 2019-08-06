# Management command which migrates between sources.
# This is not a generic management command, it's a one-off command that probably
# won't work for anything other than this one job without some changes.

import string
import csv

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from instance.models import WriteItInstance


class Command(BaseCommand):
    help = "One-off management command to change the source URL for a south-africa-assembly instance"

    def handle(self, *args, **options):
        old_url = u'https://raw.githubusercontent.com/everypolitician/everypolitician-data/master/data/South_Africa/Assembly/ep-popolo-v1.0.json'
        new_url = u'https://www.pa.org.za/api/national-assembly/popolo.json'

        id_mapping = {}
        with open(u'instance/data/people-assembly-ep-uuid-to-id-mapping.csv', u'r') as f:
            csv_file = csv.reader(f)
            for row in csv_file:
                id_mapping[row[0]] = row[1]

        try:
            instance = WriteItInstance.objects.get(slug=u'south-africa-assembly')
        except WriteItInstance.DoesNotExist:
            raise CommandError(u"Couldn't find instance")

        with transaction.atomic():
            # Change the Popolo source URL for the instance
            popolo_source = instance.writeitinstancepopitinstancerecord_set.all()[0].popolo_source
            if popolo_source.url == old_url:
                popolo_source.url = u'https://www.pa.org.za/api/national-assembly/popolo.json'
                popolo_source.save()
                self.stdout.write(u"Updated URL for {}".format(instance))

            # Update the popolo_uri identifier for people in this instance
            for instance_membership in instance.instancemembership_set.all():
                person = instance_membership.person
                popolo_uri_identifier = person.identifiers.get(scheme=u'popolo_uri')
                popolo_person_identifier = person.identifiers.get(scheme=u'popolo:person')
                ep_uuid = string.replace(popolo_uri_identifier.identifier, u"{}#person-".format(old_url), '')
                try:
                    new_id = id_mapping[ep_uuid]
                except KeyError:
                    self.stderr.write(u"Unable to find matching ID for UUID {}\n".format(ep_uuid))
                    continue
                popolo_uri_identifier.identifier = u"{}#person-{}".format(new_url, new_id)
                popolo_uri_identifier.save()
                popolo_person_identifier.identifier = new_id
                popolo_person_identifier.save()
                self.stdout.write(u"Updated identifiers for {}".format(person))
