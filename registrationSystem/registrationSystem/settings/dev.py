from registrationSystem.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'deg=*gpfq%ymtn-!ws#_g^-4r94cn=3n^=w!yig+6u%=hz#5b0'

# Debugging email. Sends email to your terminal
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
