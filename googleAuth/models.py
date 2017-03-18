from django.contrib.auth.models import User
from django.db import models
from oauth2client.contrib.django_util.models import CredentialsField

class GoogleCredentials(models.Model):
    id = models.OneToOneField(User, primary_key=True)
    credential = CredentialsField()
    class Meta:
        db_table = 'GoogleCredentials'
        verbose_name = 'Google credentials'
        verbose_name_plural = 'Google credentials'

class GoogleAuthCodes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
    class Meta:
        db_table = 'GoogleAuthCodes'
        verbose_name = 'Google auth code'
        verbose_name_plural = 'Google auth codes'
        unique_together = (
            ('user', 'code'),
        )


class GoogleUserProfiles(models.Model):
    user = models.OneToOneField(User)
    imageUrl = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'GoogleUserProfiles'
        verbose_name = 'Google User Profile'
        verbose_name_plural = 'Google User Profiles'

