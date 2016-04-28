# -*- coding: utf-8 -*-

from django.db import models

from groups.models import Group

class Exam(models.Model):

    """Exam Model"""

    class Meta(object):
        verbose_name = u"Екзамен"
        verbose_name_plural = u"Екзамени"

    name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Назва предмету")

    lector_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Ім’я викладача")

    date = models.DateTimeField(
        blank=False,
        verbose_name=u"Дата та час проведення",
        null=True)

    exam_group = models.ForeignKey(
        Group,
        verbose_name=u"Група",
        blank=False,
        null=True,
        on_delete=models.PROTECT)

    def __unicode__(self):
        return u"%s, приймає %s" % (self.name, self.lector_name)
