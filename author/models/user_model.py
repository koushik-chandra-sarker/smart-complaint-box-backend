import hashlib
from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from App.utils import send_mail, send_html_mail
from author.models.role_model import Role


class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not username:
            raise ValueError("User must have an username")
        email = email.lower()
        username = username.title()
        first_name = first_name.title()
        last_name = last_name.title()

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name

        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, first_name, last_name, password=None):
        user = self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Salutation(models.TextChoices):
    MR = 'MR', 'Mr.'
    MRS = 'MRS', 'Mrs.'
    MISS = 'MISS', 'Miss'
    MS = 'MS', 'Ms.'
    DR = 'DR', 'Dr.'
    PROF = 'PROF', 'Prof.'
    REV = 'REV', 'Rev.'
    SIR = 'SIR', 'Sir'
    MADAM = 'MADAM', 'Madam'
    BANGLA_MALE = 'BANGLA_MALE', 'জনাব'
    BANGLA_FEMALE = 'BANGLA_FEMALE', 'বেগম'
    BANGLA_SIR = 'BANGLA_SIR', 'স্যার'
    BANGLA_MADAM = 'BANGLA_MADAM', 'ম্যাডাম'
    BANGLA_DR = 'BANGLA_DR', 'ডঃ'
    BANGLA_PROF = 'BANGLA_PROF', 'প্রফেসর'
    BANGLA_BABU = 'BANGLA_BABU', 'বাবু'
    BANGLA_BIBI = 'BANGLA_BIBI', 'বিবি'


class Designation(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    roles = models.ManyToManyField(Role, blank=True)
    email = models.EmailField(max_length=200, unique=True, verbose_name='email')
    email_verified = models.BooleanField(default=False)
    username = models.CharField(max_length=200, unique=True, verbose_name='username', null=False, blank=False)
    salutation = models.CharField(max_length=15, choices=Salutation.choices)
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    office_address = models.CharField(max_length=250, help_text="Enter Your Office Address")
    personal_address = models.CharField(max_length=250, help_text="Enter Your Personal Address")
    office_phone_no = models.CharField(max_length=14, help_text="Enter Your Official Phone No")
    office_phone_verified = models.BooleanField(default=False)
    personal_phone_no = models.CharField(max_length=14, help_text="Enter Your Personal Phone No")
    personal_phone_verified = models.BooleanField(default=False)
    nid_no = models.CharField(max_length=250, help_text="Enter Your National Id Card Number.")
    profile_pic = models.ImageField(default='profile-pic-default.jpg', upload_to='profile_picture')
    designation = models.ForeignKey(Designation, null=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', "username")

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     return self.is_superuser
    #
    # def has_module_perms(self, app_label):
    #     return self.is_superuser

    class Meta:
        verbose_name_plural = 'Users'


class EmailConfirmed(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=500)
    email_confirm = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = 'User Email Confirm'


@receiver(post_save, sender=User)
def create_user_email_confirmation(sender, instance, created, **kwargs):
    if created:
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        email_confirm_instance = EmailConfirmed(user=instance)
        user_encoded = f'{instance.email}-{dt}'.encode()
        activation_key = hashlib.sha224(user_encoded).hexdigest()
        email_confirm_instance.activation_key = activation_key
        email_confirm_instance.save()
        send_html_mail(instance.email, "/author/verify-mail/?token=" + activation_key, "test url", "Confirm Email")
