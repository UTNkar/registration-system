from django.contrib.auth.models import UserManager
from django.utils import timezone


class CommonUserManager(UserManager):
    def get_by_natural_key(self, person_nr):
        return self.get(person_nr=person_nr)

    def __create_user(self, person_nr, name, email, phone_nr, is_utn_member,
                      password, is_superuser, is_staff, belongs_to_group):
        now = timezone.now()
        if not person_nr:
            raise ValueError('Person number is required.')
        email = UserManager.normalize_email(email)
        user = self.model(
            person_nr=person_nr,
            email=email,
            name=name,
            phone_nr=phone_nr,
            password=password,
            is_utn_member=is_utn_member,
            is_superuser=is_superuser,
            is_staff=is_staff if is_staff else is_superuser,
            last_login=now,
            belongs_to_group=belongs_to_group
        )

        user.set_password(password)
        user.save()
        return user

    def create_user(self, person_nr, name, email, phone_nr, is_utn_member,
                    password, belongs_to_group=None):
        """
        Creates a non-superuser identified by person_nr
        """
        return self.__create_user(person_nr, name, email, phone_nr,
                                  is_utn_member, password,
                                  is_superuser=False, is_staff=False,
                                  belongs_to_group=belongs_to_group)

    def create_superuser(self, person_nr, name, email, phone_nr, is_utn_member,
                         password, belongs_to_group=None):
        """
        Creates a superuser identified by person_nr
        """
        return self.__create_user(person_nr, name, email, phone_nr,
                                  is_utn_member, password,
                                  is_superuser=True, is_staff=True,
                                  belongs_to_group=belongs_to_group)
