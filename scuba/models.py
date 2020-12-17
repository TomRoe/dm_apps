from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

from lib.templatetags.custom_filters import nz
from shared_models import models as shared_models
from shared_models.models import SimpleLookup, UnilingualSimpleLookup, UnilingualLookup


class Region(UnilingualLookup):
    description_en = models.TextField(blank=True, null=True, verbose_name=_("description (EN)"))
    description_fr = models.TextField(blank=True, null=True, verbose_name=_("description (FR)"))
    province = models.ForeignKey(shared_models.Province, on_delete=models.DO_NOTHING, related_name='scuba_regions', blank=True, null=True)

    def __str__(self):
        mystr = self.name
        if self.province:
            mystr += f" {self.tdescription}"
        return mystr


class Site(UnilingualLookup):
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, related_name='sites')
    latitude_n = models.FloatField(blank=True, null=True)
    longitude_w = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.tname} ({self.region})"



class Sample(models.Model):
    site = models.ForeignKey(Site, related_name='samples', on_delete=models.DO_NOTHING)
    start_date = models.DateTimeField(verbose_name="Start date / time (yyyy-mm-dd hh:mm)")
    end_date = models.DateTimeField(blank=True, null=True, verbose_name="End date / time (yyyy-mm-dd hh:mm)")
#     weather_notes = models.CharField(max_length=1000, blank=True, null=True)
#     rain_past_24_hours = models.BooleanField(default=False, verbose_name="Has it rained in the past 24 h?")
#     h2o_temperature_c = models.FloatField(null=True, blank=True, verbose_name="Water temperature (°C)")
#     salinity = models.FloatField(null=True, blank=True, verbose_name="Salinity (ppt)")
#     dissolved_o2 = models.FloatField(null=True, blank=True, verbose_name="dissolved oxygen (mg/L)")
#     water_turbidity = models.IntegerField(choices=TURBIDITY_CHOICES, blank=True, null=True)
#     tide_state = models.CharField(max_length=5, choices=TIDE_STATE_CHOICES, blank=True, null=True)
#     tide_direction = models.CharField(max_length=5, choices=TIDE_DIR_CHOICES, blank=True, null=True)
#     samplers = models.CharField(max_length=1000, blank=True, null=True)
#
#     percent_sand = models.FloatField(null=True, blank=True, verbose_name="Sand (%)")
#     percent_gravel = models.FloatField(null=True, blank=True, verbose_name="Gravel (%)")
#     percent_rock = models.FloatField(null=True, blank=True, verbose_name="Rock (%)")
#     percent_mud = models.FloatField(null=True, blank=True, verbose_name="Mud (%)")
#
#     visual_sediment_obs = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Visual sediment observations")
#     sav_survey_conducted = models.BooleanField(default=False, verbose_name="Was SAV survey conducted?")
#     excessive_green_algae_water = models.BooleanField(default=False, verbose_name="Excessive green algae in water?")
#     excessive_green_algae_shore = models.BooleanField(default=False, verbose_name="Excessive green algae on shore?")
#     unsampled_vegetation_inside = models.CharField(max_length=1000, blank=True, null=True,
#                                                    verbose_name="Vegetation present inside sample area (underwater) but outside of quadrat")
#     unsampled_vegetation_outside = models.CharField(max_length=1000, blank=True, null=True,
#                                                     verbose_name="Vegetation present outside of sample area (underwater)")
#
#     per_sediment_water_cont = models.FloatField(null=True, blank=True, verbose_name="sediment water content (%)")
#     per_sediment_organic_cont = models.FloatField(null=True, blank=True, verbose_name="sediment organic content (%)")
#     mean_sediment_grain_size = models.FloatField(null=True, blank=True,
#                                                  verbose_name="Mean sediment grain size (??)")  # where 9999 means >2000
#
#     silicate = models.FloatField(null=True, blank=True, verbose_name="Silicate (µM)")
#     phosphate = models.FloatField(null=True, blank=True, verbose_name="Phosphate (µM)")
#     nitrates = models.FloatField(null=True, blank=True, verbose_name="NO3 + NO2(µM)")
#     nitrite = models.FloatField(null=True, blank=True, verbose_name="Nitrite (µM)")
#     ammonia = models.FloatField(null=True, blank=True, verbose_name="Ammonia (µM)")
#     notes = models.TextField(blank=True, null=True)
#
#     year = models.IntegerField(null=True, blank=True)
#     month = models.IntegerField(null=True, blank=True)
#     last_modified = models.DateTimeField(blank=True, null=True)
#     species = models.ManyToManyField(Species, through="SpeciesObservation")
#
#     def save(self, *args, **kwargs):
#         self.year = self.start_date.year
#         self.month = self.start_date.month
#         self.last_modified = timezone.now()
#
#         super().save(*args, **kwargs)
#
#     class Meta:
#         ordering = ['-start_date', 'station']
#         unique_together = [["start_date", "station"], ]
#
#     def get_absolute_url(self):
#         return reverse("camp:sample_detail", kwargs={"pk": self.id})
#
#     def __str__(self):
#         return "Sample {}".format(self.id)
#
#
# class SpeciesObservation(models.Model):
#     species = models.ForeignKey(Species, on_delete=models.DO_NOTHING, related_name="sample_spp")
#     sample = models.ForeignKey(Sample, on_delete=models.DO_NOTHING, related_name="sample_spp")
#     adults = models.IntegerField(blank=True, null=True)
#     yoy = models.IntegerField(blank=True, null=True, verbose_name="young of the year (YOY)")
#     total_non_sav = models.IntegerField(null=True, blank=True)
#     total_sav = models.FloatField(blank=True, null=True, verbose_name="SAV level")  # this is reserved only for SAV
#
#     def save(self, *args, **kwargs):
#         self.total_non_sav = nz(self.adults, 0) + nz(self.yoy, 0)
#         return super().save(*args, **kwargs)
#
#     class Meta:
#         unique_together = [["sample", "species"], ]
#         # ordering = ["-sample__year"] THIS IS WAY TOO SLOW!
