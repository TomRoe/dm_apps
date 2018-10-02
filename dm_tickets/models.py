from django.db import models
from django.utils import timezone
from django.urls import reverse
# import misaka
import markdown
# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        ordering = ['first_name', 'last_name']

    @property
    def full_name(self):
        return "{} {}".format(self.first_name,self.last_name)

    def get_absolute_url(self):
        return reverse('tickets:person_detail', kwargs={'pk':self.id})

class Section(models.Model):
    section_name = models.CharField(max_length=255)

    def __str__(self):
        return self.section_name

    class Meta:
        ordering = ['section_name']

class RequestType(models.Model):
    request_type = models.CharField(max_length=255)

    def __str__(self):
        return self.request_type


class ServiceDeskTicket(models.Model):
    ref_number = models.CharField(max_length=8)
    ticket_url = models.URLField(null=True, blank=True)
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    description = models.TextField(null=True,blank=True)
    date_logged = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.description:
            if self.description.__len__() > 125:
                my_descr = self.description[:125]+" ..."
            else:
                my_descr = self.description
            my_str = "{} - {}".format(self.ref_number, my_descr)
        else:
            my_str = self.ref_number
        return my_str


    def get_absolute_url(self):
        return reverse('tickets:sd_detail', kwargs={'pk':self.id})

    class Meta:
        ordering = ['-ref_number']

class Tag(models.Model):
    tag = models.CharField(max_length=255)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tickets:tag_detail', kwargs={'pk':self.id})

    class Meta:
        ordering = ['tag']


class Ticket(models.Model):
    # Choices for status
    RESOLVED = '2'
    ACTIVE = '5'
    IDLE = '6'
    UNRESOLVED = '7'
    STATUS_CHOICES = (
        (ACTIVE,'Active'),
        (RESOLVED,'Resolved'),
        (IDLE,'Idle'),
        (UNRESOLVED,'Unresolved'),
    )

    # Choices for priority
    HIGH = '1'
    MED = '2'
    LOW = '3'
    WISHLIST = '4'
    URGENT = '5'
    PRIORITY_CHOICES = (
        (HIGH,'High'),
        (MED,'Medium'),
        (LOW,'Low'),
        (WISHLIST,'Wish List'),
        (URGENT,'Urgent'),
    )

    title = models.CharField(max_length=255)
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)
    status = models.CharField( default=ACTIVE, max_length=1, choices=STATUS_CHOICES )
    priority = models.CharField(default=HIGH, max_length=1, choices=PRIORITY_CHOICES )
    request_type = models.ForeignKey(RequestType, on_delete=models.DO_NOTHING)
    description = models.TextField(blank=True,null=True)
    service_desk_ticket = models.ForeignKey(ServiceDeskTicket, blank=True,null=True, on_delete=models.DO_NOTHING)
    financial_coding = models.CharField(max_length=100, blank=True,null=True )
    notes = models.TextField(blank=True,null=True)
    notes_html = models.TextField(blank=True,null=True)
    date_opened = models.DateTimeField(default=timezone.now)
    date_closed = models.DateTimeField(null=True, blank=True)
    date_modified = models.DateTimeField(default=timezone.now)
    people = models.ManyToManyField(Person, related_name='tickets')
    tags = models.ManyToManyField(Tag)
    primary_contact = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    resolved_email_date = models.DateTimeField(null=True, blank=True)

    def save(self,*args,**kwargs):
        if self.notes:
            self.notes_html = markdown.markdown(self.notes)

        self.date_modified = timezone.now()
        if self.date_closed:
            self.status = '2'
        else:
            if self.status == None:
                self.status = '5'

        super().save(*args,**kwargs)

    class Meta:
        ordering = ['-date_modified']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tickets:detail', kwargs={'pk':self.id})

    @property
    def search_clob(self):
        return "{} {} {} {} {} {}".format(self.title, self.description, self.service_desk_ticket, self.request_type, self.people.all(), self.tags.all())

    @property
    def tags_pretty(self):
        my_str  = ""
        for tag in self.tags.all():
            my_str = my_str + tag.tag + ", "

        return my_str[:len(my_str)-2]

    @property
    def people_pretty(self):
        my_str  = ""
        for person in self.people.all():
            my_str = my_str + "{} {},<br>".format(person.first_name, person.last_name)

        return my_str[:len(my_str)-5]

def ticket_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'dm_tickets/ticket_{0}/{1}'.format(instance.ticket.id, filename)

class File(models.Model):
    caption = models.CharField(max_length=255)
    ticket = models.ForeignKey(Ticket, related_name="files", on_delete=models.CASCADE)
    file = models.FileField(upload_to=ticket_directory_path)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.caption

    def get_absolute_url(self):
        return reverse('tickets:file_detail', kwargs={
            'ticket':self.ticket.id,
            'pk':self.id
        })
