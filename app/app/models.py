# -*- coding: utf-8 -*-
from django.db import models

class Servers(models.Model):
    server_id = models.CharField(max_length=90, primary_key=True, blank=False, unique=True)
    #True means task in progress, False means running task
    server_status = models.BooleanField(blank=True, default=False)

    def __unicode__(self):
        return str(self.server_id)
