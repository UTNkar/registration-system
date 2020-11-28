from django.test import TestCase
from django.core.exceptions import ValidationError
from registrationSystem.validators import SSNValidator


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
