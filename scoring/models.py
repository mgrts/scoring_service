from django.db import models


class LogRegModel(models.Model):

    name = models.CharField(max_length=30, help_text='Name of a scoring model')
    sql_text = models.TextField(max_length=100000, help_text='SQL request for scoring')

    def __str__(self):
        return self.name
