# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    # user mapping
    user = models.OneToOneField(User)

    class Meta(object):
        verbose_name = (u"User Profile")

    # extra user data
    mobile_phone = models.CharField(
        max_length=12,
        blank=True,
        verbose_name=(u"Mobile Phone"),
    default='')


def __unicode__(self):
    return self.user.username
