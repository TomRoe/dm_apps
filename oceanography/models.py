import os
from django.dispatch import receiver
from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.

def img_file_name(instance, filename):
    img_name = 'oceanography/{}'.format(filename)
    return img_name

class Doc(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    source = models.TextField(null=True, blank=True)
    # url = models.TextField(null=True, blank=True)
    file = models.FileField(null=True, blank=True, upload_to=img_file_name)
    date_modified = models.DateTimeField(default = timezone.now )

    def save(self,*args,**kwargs):
        self.date_modified  = timezone.now()
        return super().save(*args,**kwargs)


    def __str__(self):
        return self.item_name

class Probe(models.Model):
    probe_name = models.CharField(max_length=255)

    def __str__(self):
        return self.probe_name

class Institute(models.Model):
    name = models.CharField(max_length=255)
    abbrev = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Vessel(models.Model):
    name = models.CharField(max_length=255)
    call_sign = models.CharField(max_length=56, null=True, blank=True)

    def __str__(self):
        if self.call_sign:
            return "{} {}".format(self.name, self.call_sign)
        else:
            return "{}".format(self.name)


    class Meta:
        ordering = ['name',]

class Mission(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.DO_NOTHING, blank=True, null=True)
    mission_name = models.CharField(max_length=255)
    mission_number = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    # vessel_name = models.CharField(max_length=255)
    # ship_call_sign = models.CharField(max_length=255, null=True, blank=True)
    chief_scientist = models.CharField(max_length=255)
    samplers = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    probe = models.ForeignKey(Probe, null=True, blank=True, on_delete=models.DO_NOTHING)
    area_of_operation = models.CharField(max_length=255, null=True, blank=True)
    number_of_profiles = models.IntegerField()
    meds_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="MEDS ID")
    notes = models.CharField(max_length=255, null=True, blank=True)
    season = models.IntegerField(null=True, blank=True)
    vessel = models.ForeignKey(Vessel, on_delete=models.DO_NOTHING, related_name="missions", blank=True, null=True)

    def save(self,*args,**kwargs):
        if self.start_date:
            self.season = self.start_date.year
        return super().save(*args,**kwargs)


class Bottle(models.Model):

    # Choices for sal_units
    PPT = "PPT"
    PSU = "PSU"
    SAL_UNITS_CHOICES = (
        (PPT, "parts per thousand (PPT)"),
        (PSU, "practical salinity unit (PSU)"),
    )

    # Choices for timezone
    TIMEZONE_CHOICES = (
        ("AST","Atlantic Standard Time"),
        ("ADT","Atlantic Daylight Time"),
        ("UTC","Coordinated Universal Time"),
    )

    mission = models.ForeignKey(Mission, related_name="bottles", on_delete=models.CASCADE)
    bottle_uid = models.CharField(max_length=10, unique=True)
    station = models.CharField(null=True, blank=True, max_length=25, verbose_name="Station")
    stratum = models.IntegerField(null=True, blank=True, verbose_name="Stratum")
    set = models.IntegerField(null=True, blank=True, verbose_name="Set #")
    event = models.CharField(max_length=510, null=True, blank=True)
    date_time = models.DateTimeField(null=True, blank=True)
    timezone = models.CharField(max_length=3, choices=TIMEZONE_CHOICES)
    date_time_UTC = models.DateTimeField(null=True, blank=True, verbose_name="Date / time (UTC)")
    sounding_m = models.FloatField(null=True, blank=True, verbose_name="Sounding (m)")
    bottle_depth_m = models.FloatField(null=True, blank=True, verbose_name="Bottle depth (m)")
    temp_c = models.FloatField(null=True, blank=True, verbose_name="Temperature (°C)")
    salinity = models.FloatField(null=True, blank=True, verbose_name="Salinity")
    sal_units = models.CharField(max_length=5, null=True, blank=True, choices=SAL_UNITS_CHOICES, verbose_name="Salinity units")
    ph = models.FloatField(null=True, blank=True, verbose_name="pH")
    lat_DDdd = models.FloatField(null=True, blank=True, verbose_name="Latitude")
    long_DDdd = models.FloatField(null=True, blank=True, verbose_name="Longitude")
    ctd_filename = models.CharField(max_length=255, null=True, blank=True)
    remarks = models.CharField(max_length=510, null=True, blank=True)
    samples_collected = models.CharField(max_length=510, null=True, blank=True)

    def save(self,*args,**kwargs):
        if self.date_time and self.timezone:
            if self.timezone == "UTC":
                self.date_time_UTC  = self.date_time
            elif self.timezone == "AST":
                self.date_time_UTC  = self.date_time + timedelta(hours=4)
            elif self.timezone == "ADT":
                self.date_time_UTC  = self.date_time + timedelta(hours=3)
        return super().save(*args,**kwargs)

    class Meta:
        ordering = ['mission','bottle_uid']

def file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'oceanography/{0}/{1}'.format(instance.mission.mission_number, filename)

class File(models.Model):
    caption = models.CharField(max_length=255)
    mission = models.ForeignKey(Mission, related_name="files", on_delete=models.CASCADE)
    file = models.FileField(upload_to=file_directory_path)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.caption


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

@receiver(models.signals.pre_save, sender=File)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = File.objects.get(pk=instance.pk).file
    except File.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
