from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager
#from django.contrib.postgres.fields import JSONField


class Questionnaire(models.Model):
    user_pk = models.IntegerField()
    landlord_pk = models.IntegerField()
    placementValue = models.IntegerField()
    contractConditionsValue = models.IntegerField()
    futureParthershipValue = models.IntegerField()
    qualityValue = models.IntegerField()
    politenessValue = models.IntegerField()
    currentSituationValue = models.IntegerField()
    communicationValue = models.IntegerField()
    recommendationValue = models.IntegerField()
    expectationsValue = models.IntegerField()
    safetyValue = models.IntegerField()
    review = models.TextField(max_length = 5000, default = None)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=30)
    is_renter = models.BooleanField(default=True)
    is_landlord = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    questionnaires = models.ManyToManyField(Questionnaire)
    clients = models.ManyToManyField('self', default = None) #landlords for renter, renters for landlords
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    def __str__(self):
        return self.email



class Message(models.Model):
    author_name = models.CharField(max_length = 50)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default = None)
    chat_pk = models.IntegerField(default = -1) #если сообщение забанено, например
    #poll_pk = models.IntegerField(default = -1)

    def __str__(self):
        return self.content

    def numberToShow(self, number):
        ans = str(number)
        if(number < 10):
            ans = "0" + ans
        return ans

    def getTime(self):
        return {
            'year': self.timestamp.year,
            'month': self.numberToShow(self.timestamp.month),
            'day': self.numberToShow(self.timestamp.day),
            'hours': self.numberToShow(self.timestamp.hour),
            'minutes': self.numberToShow(self.timestamp.minute),
        }


class Chat(models.Model):
    name = models.TextField(max_length = 100)
    messages = models.ManyToManyField(Message, blank = True, default = None, related_name="messages")
    landlord = models.OneToOneField(CustomUser, primary_key = True, on_delete = models.CASCADE)
    users = models.ManyToManyField(CustomUser, related_name="Chat_users")
    moderator_pk = models.IntegerField(default = -1)

    def __str__(self):
        return self.name


class LastReadMessage(models.Model):
    user_pk = models.IntegerField()
    chat_pk = models.IntegerField()
    message_pk  = models.IntegerField(default = -1)

    def __str__(self):
        return "user_pk: " + str(self.user_pk) + "; chat_pk: " + str(self.chat_pk) + "; message_pk: " + str(self.message_pk)

# class PollResult(models.Model):
#     poll_pk  = models.IntegerField()
#     user_pk = models.IntegerField()
#     result = models.IntegerField()
#
# class Poll1(models.Model):
#     message = models.OneToOneField(Message, primary_key = True, on_delete = models.CASCADE)
#     votes = models.ManyToManyField(PollResult, blank = True)
