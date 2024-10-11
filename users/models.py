from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
# from django_cryptography.fields import encrypt


class UserManager(BaseUserManager):
    def create_user(self, user_id, email, username, name, password=None):
        if not user_id:
            raise ValueError('users must have an id')
        if not email:
            raise ValueError('users must have an email')
        if not username:
            raise ValueError('users must have an username')
        if not name:
            raise ValueError('users must have a name')
        

        user = self.model(
            user_id = user_id,
            email = self.normalize_email(email),
            username = username,
            name = name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, email, username, name, password):
        user = self.create_user(
            user_id = user_id,
            email = self.normalize_email(email),
            username = username,
            password = password,
            name = name
        )
        
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser):
    user_id = models.CharField(verbose_name='user id',
				  max_length=8, 
                                  unique=True, 
                                  null=False, 
                                  blank=False)
    email = models.EmailField(verbose_name='email',
			      max_length=254, 
                              unique=True, 
                              null=False, 
                              blank=False)
    username = models.CharField(max_length=30, 
                                unique=True, 
                                null=False, 
                                blank=False)
    name = models.CharField(max_length=225, null=False, blank=False)
    date_joined = models.DateTimeField(auto_now_add=True, null=False)
    last_login = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_id', 'username', 'name']

    objects = UserManager()


    def __str__(self):
        return f"{self.username}"
    

    def has_perm(self, perm, obj=None):
        return self.is_admin
    

    def has_module_perms(self, app_label):
        return True


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
                                related_name='profile', 
                                on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')


    def __str__(self):
        return f"{self.user.username}'s profile"


class Wallet(models.Model):
    owner = models.OneToOneField('Profile', 
                                  related_name='wallet', 
                                  blank=True, 
                                  null=True,
                                  on_delete=models.CASCADE)
    seed_phrase = models.CharField(max_length=255, null=False, blank=False, unique=True)
    external_wallet = models.CharField(max_length=255, blank=False, null=False)


    def __str__(self):
        return f"{self.owner.user.username}'s wallet"


class Fund(models.Model):
    amount = models.IntegerField(null=False, blank=False)
    owner = models.ForeignKey(Profile, related_name='funds', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')


    def __str__(self):
        return f"new fund for {self.owner.user.name}"
    

    def save(self, *args, **kwargs):
        self.owner.balance += self.amount
        self.owner.save()
        super(Fund, self).save(*args, **kwargs)
        



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created=False, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance,  **kwargs):
    instance.profile.save()
