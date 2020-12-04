from django.test import TestCase
from django.core.exceptions import ValidationError
from registrationSystem.validators import SSNValidator
from registrationSystem.forms import RaffleEntryForm
from registrationSystem.models import RaffleEntry


class SSNValidatorTest(TestCase):
    def test_long_ssn(self):
        try:
            SSNValidator()("19980521-1234")
        except ValidationError:
            self.fail("Valid SSN raised a validation error")

    def test_long_ssn_with_t(self):
        try:
            SSNValidator()("19980521-T234")
            SSNValidator()("19980521-t234")
        except ValidationError:
            self.fail("Valid SSN raised a validation error")

    def test_long_ssn_without_dash(self):
        with self.assertRaises(ValidationError):
            SSNValidator()("199805211234")

    def test_short_ssn(self):
        with self.assertRaises(ValidationError):
            SSNValidator()("980521-1234")

    def test_short_ssn_without_dash(self):
        with self.assertRaises(ValidationError):
            SSNValidator()("9805211234")


class RaffleEntryFormTest(TestCase):
    raffle_entry_1 = {
        'name': 'Namn namnsson',
        'email': 'mail@mail.se',
        'person_nr': '19980521-1234',
        'is_utn_member': True
    }

    def setUp(self):
        raffle_entry = RaffleEntry.objects.create(**self.raffle_entry_1)
        raffle_entry.save()

    def test_create_new_raffle_entry(self):
        new_raffle = {
            'name': 'Namnet namn',
            'email': 'mail2@mail2.se',
            'person_nr': '19980322-1234',
            'is_utn_member': True
        }
        form = RaffleEntryForm(data=new_raffle)
        self.assertTrue(form.is_valid())

        raffle_entry, created = form.save()
        self.assertTrue(created)

    def test_correct_ssn_incorrect_mail(self):
        new_raffle = {
            'name': 'Bengt namnsson',
            'email': 'apa@bp.se',
            'person_nr': '19980521-1234',
            'is_utn_member': True
        }
        form = RaffleEntryForm(data=new_raffle)
        self.assertFalse(form.is_valid())

        self.assertEqual(form.errors, {
            '__all__': ["A Person number with that email could not be found"]
        })

    def test_incorrect_ssn_correct_mail(self):
        new_raffle = {
            'name': 'Bengt namnsson',
            'email': 'mail@mail.se',
            'person_nr': '19980411-1234',
            'is_utn_member': True
        }
        form = RaffleEntryForm(data=new_raffle)
        self.assertFalse(form.is_valid())

        self.assertEqual(form.errors, {
            '__all__': ["That email has already been used"]
        })
