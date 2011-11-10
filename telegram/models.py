from django.db import models
from django.contrib.auth.models import User

DEBUG = 1
INFO = 2
SUCCESS = 3
WARNING = 4
ERROR = 5
CRITICAL = 6

LEVEL_CHOICES = (
        (DEBUG, 'DEBUG'),
        (INFO, 'INFO'),
        (SUCCESS, 'SUCCESS'),
        (WARNING, 'WARNING'),
        (ERROR, 'ERROR'),
        (CRITICAL, 'CRITICAL'),
)


class Subscription(models.Model):

    user = models.ForeignKey(User)
    message_channel = models.ForeignKey('Channel')
    level = models.IntegerField(default=INFO,
            choices=LEVEL_CHOICES)
    platforms = models.ManyToManyField('Platform',
            through='SubscriptionPlatform')
    disabled = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s subscribed to: %s' % (self.user.username, self.message_channel.name)


class SubscriptionMeta(models.Model):

    value = models.TextField()
    subscription = models.ForeignKey('Subscription')

    def __unicode__(self):
        return self.value


class Channel(models.Model):

    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Platform(models.Model):

    name = models.CharField(max_length=255)
    handler = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class SubscriptionPlatform(models.Model):

    subscription = models.ForeignKey('Subscription')
    platform = models.ForeignKey('Platform')


class Telegram(models.Model):

    channel = models.ForeignKey('Channel')
    subject = models.CharField(max_length=255)
    content = models.TextField()
    level = models.IntegerField(choices=LEVEL_CHOICES)
    created_at = models.DateTimeField(auto_now=True)


class SendLog(models.Model):

    telegram = models.ForeignKey('Telegram')
    subscription_platform = models.ForeignKey('SubscriptionPlatform')
    sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)