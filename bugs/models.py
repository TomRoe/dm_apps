from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.

class Bug(models.Model):
    # Choices for importance

    URGENT = 'u'
    HIGH = 'h'
    MED = 'm'
    LOW = 'l'
    WISHLIST = 'w'
    QC_ELEMENT = 'q'

    IMPORTANCE_CHOICES = (
        (URGENT,'Urgent'),
        (HIGH,'High'),
        (MED,'Medium'),
        (LOW,'Low'),
        (WISHLIST,'Wishlist'),
        (QC_ELEMENT,'Quality control element')
    )


    # Choices for application

    GENERAL = 1
    GRAIS = 2
    INVENTORY = 3
    HERMORRHAGE = 4
    RDMTS = 5
    ACCOUNTS = 6

    APP_CHOICES = (
        (GENERAL,'General'),
        (ACCOUNTS,'Accounts'),
        (GRAIS,'grAIS'),
        (INVENTORY,'Data Inventory'),
        (HERMORRHAGE,'HerMorrhage'),
        (RDMTS,'Ticketing System'),
    )

    APP_DICT = {
        GENERAL:'General',
        ACCOUNTS:'Accounts',
        GRAIS:'grAIS',
        INVENTORY:'Data Inventory',
        HERMORRHAGE:'HerMorrhage',
        RDMTS:'Ticketing System',
    }

    user = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    application = models.IntegerField(choices=APP_CHOICES)
    date_created = models.DateTimeField(default=timezone.now)
    importance = models.CharField(max_length=1, choices=IMPORTANCE_CHOICES)
    subject = models.CharField(max_length=255)
    detail = models.TextField(blank=True, null=True)
    date_resolved = models.DateTimeField(db_column='DATE_RESOLVED', blank=True, null=True)
    resolved = models.BooleanField(default = False)

    def save(self,*args,**kwargs):
        if self.date_resolved == None:
            self.resolved = False
        else:
            self.resolved = True

        super().save(*args,**kwargs)

    class Meta:
        ordering = ['resolved','application','-date_created']