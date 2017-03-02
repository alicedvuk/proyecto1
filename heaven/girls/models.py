from django.db import models
from django.conf import settings
# Create your models here.

class Girl(models.Model):
    GIRL_INCALL = 1
    GIRL_OUTCALL = 2
    GIRL_EX = 3

    GIRL_STATUSES = (
        (GIRL_INCALL, 'Incall Girl'),
        (GIRL_OUTCALL, 'Outcall Girl'),
        (GIRL_EX, 'Ex Girl'),

    )
    status = models.IntegerField('Status', default=GIRL_INCALL,choices=GIRL_STATUSES, db_index=True )
    name = models.CharField('Name Girl', max_length=50, null=True,)
    phone = models.CharField('Phone number', max_length=20, null=True,)
    mobile_phone = models.CharField('Mobile Phone number', max_length=20, null=True, blank = True,)
    postcode = models.CharField('Postcode', max_length=50, null=True,)
    address = models.CharField('Adress', max_length=50, null=True, )
    flat = models.CharField('Flat', max_length=20, null=True, blank = True, )
    tube_station = models.CharField('Tube Station ', max_length=50, null=True, blank = True,)
    email = models.CharField( 'Email', max_length=50, null=True, blank = True,  )
    live_with = models.CharField( 'Live With', max_length=90,  null=True, blank = True,    )
    date = models.DateTimeField(verbose_name='Date started working')

    def __str__(self):
        return self.verbose_name

    @property
    def verbose_name(self):
        return self.name
    