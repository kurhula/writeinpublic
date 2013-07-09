from global_test_case import GlobalTestCase as TestCase
from django.utils.unittest import skip
from contactos.models import ContactType, Contact
from popit.models import Person, ApiInstance
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class ContactTestCase(TestCase):
    def setUp(self):
        super(ContactTestCase,self).setUp()
        self.person = Person.objects.all()[0]
        self.user = User.objects.all()[0]

    def test_create_contact_type(self):
        contact_type = ContactType.objects.create(name='mental message', label_name = 'mental address id')
        self.assertTrue(contact_type)
        self.assertEquals(contact_type.name, 'mental message')
        self.assertEquals(contact_type.label_name, 'mental address id')

    def test_contact_type_unicode(self):
        contact_type = ContactType.objects.create(name='mental message', label_name = 'mental address id')
        self.assertEquals(contact_type.__unicode__(), contact_type.label_name)

    def test_create_contact(self):
        contact_type = ContactType.objects.create(name='mental message', label_name = 'mental address id')
        contact1 = Contact.objects.create(contact_type= contact_type, value = 'contact point', person= self.person, owner=self.user)
        self.assertTrue(contact1)
        self.assertFalse(contact1.is_bounced)
        self.assertEquals(contact1.contact_type, contact_type)
        self.assertEquals(contact1.value, 'contact point')
        self.assertEquals(contact1.person, self.person)

    def test_contact_unicode(self):
        contact_type = ContactType.objects.create(name='mental message', label_name = 'mental address id')
        contact1 = Contact.objects.create(contact_type= contact_type, value = 'contact point', person= self.person, owner=self.user)
        expected_unicode = _('%(contact)s (%(type)s)') % {
            'contact':contact1.value,
            'type':contact_type.label_name
        }

        self.assertEquals(contact1.__unicode__(), expected_unicode)

    def test_contact_has_owner(self):
        contact_type = ContactType.objects.create(name='mental message', label_name = 'mental address id')
        user = User.objects.all()[0]
        contact1 = Contact.objects.create(contact_type= contact_type, value = 'contact point', person= self.person, owner= user)
        
        self.assertEquals(contact1.owner, user)

