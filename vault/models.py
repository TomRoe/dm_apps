from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from shared_models import models as shared_models


class Species(models.Model):
    code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("Internal code"), unique=True)
    english_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("English name"))
    french_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("French name"))
    latin_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Scientific name"))
    vor_code = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("VOR code"))
    quebec_code = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Quebec code"))
    maritimes_code = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Maritimes code"))
    aphia_id = models.IntegerField(null=True, blank=True, verbose_name=_("ID in World Registry of Marine Species"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("english_name"))):

            return "{}".format(getattr(self, str(_("english_name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.english_name)

    def get_absolute_url(self):
        return reverse("vault:species_detail", kwargs={"pk": self.id})

class Role(models.Model):
    name = models.CharField(max_length=255)
    nom = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):

            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]

class Organisation(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("English name"))
    abbrev_name = models.CharField(max_length=255, verbose_name=_("English abbreviated name"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("French name"))
    abbrev_nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("French abbreviated name"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):

            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)



class Person(models.Model):
    first_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("First name"))
    last_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Last name"))
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="people", verbose_name=_("Organisation"), null=True, blank=True)
    email = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Email address"))
    phone = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Phone number"))
    roles = models.ManyToManyField(Role, verbose_name=_("Roles"))

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse("vault:person_detail", kwargs={"pk": self.id})


class MetadataField(models.Model):
    DATA_TYPE_CHOICES = (
        (1, _("integer/categorical")),
        (2, _("float")),
        (3, _("string")),
    )
    name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Name"))
    nom = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Nom"))
    description_eng = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("English description"))
    description_fra = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("French description"))
    data_type = models.IntegerField(choices=DATA_TYPE_CHOICES, verbose_name=_("data type"))

    def __str__(self):
        return self.name

# used for defining metadata field categories, when applicable
class MetadataFieldCategory(models.Model):
    metadata_field = models.ForeignKey(MetadataField, on_delete=models.CASCADE, related_name="categories")
    code = models.CharField(max_length=3)
    description_eng = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("English description"))
    description_fra = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("French description"))

    @property
    def tname(self):
        # check to see if a french value is given
        if getattr(self, str(_("description_eng"))):
            return "{}".format(getattr(self, str(_("description_eng"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.description_eng)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("description_eng"))):
            return "{}-{}".format(self.code, getattr(self, str(_("description_eng"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}-{}".format(self.code, self.description_eng)

    class Meta:
        ordering = ['code', ]
        unique_together = ['metadata_field', 'code']


class InstrumentType(models.Model):
    mode = models.CharField(max_length=255, verbose_name=_("Mode"))
    type = models.CharField(max_length=255, verbose_name=_("Mode type"))
    name = models.CharField(max_length=255, verbose_name=_("English name"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("French name"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):

            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)


class Instrument(models.Model):
    instrument_type = models.ForeignKey(InstrumentType, on_delete=models.DO_NOTHING, related_name="instruments",
                                                  verbose_name=_("Type of instrument"))
    name = models.CharField(max_length=255, verbose_name=_("English name"))
    nom = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("French name"))
    #metadata = models.ManyToManyField("MetadataField", through="InstrumentMetadatum",  verbose_name=_("Metadata"))

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):

            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    def get_absolute_url(self):
        return reverse("vault:instrument_detail", kwargs={"pk": self.id})

class InstrumentMetadatum(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.DO_NOTHING, related_name="instrument_metadata",
                                   verbose_name=_("instrument"))
    metadata_field = models.ForeignKey("MetadataField", on_delete=models.CASCADE, related_name="instrument_metadata")
    value = models.CharField(max_length=1000)


# CHOICES = plane, boat, drone, mooring, glider, land, space
class ObservationPlatformType(models.Model):
    name = models.CharField(max_length=255)
    nom = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):

            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['id', ]


class ObservationPlatform(models.Model):
    observation_platform_type = models.ForeignKey(ObservationPlatformType, on_delete=models.DO_NOTHING, related_name="platforms",
                                                  verbose_name=_("Type of observation platform"))
    authority = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="platform_authorities", verbose_name=_("authority"), null=True, blank=True)
    owner = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="platform_owners", verbose_name=_("owner"), null=True, blank=True)
    make_model = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Make and model"))
    name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Call name"))
    longname = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_("Long name"))

    @property
    def foldername(self):
        return  "{}_{}_{}".format(self.authority.abbrev_name, self.owner.abbrev_name, self.name)


    def __str__(self):
        return "{}".format(self.longname)

    def get_absolute_url(self):
        return reverse("vault:observationplatform_detail", kwargs={"pk":self.id})

class Outing(models.Model):
    observation_platform = models.ForeignKey(ObservationPlatform, on_delete=models.DO_NOTHING, related_name="outings",
                                             verbose_name=_("observation platform"))
    region = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Region"))
    purpose = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Purpose"))
    start_date = models.DateTimeField(blank=True, null=True, verbose_name=_("Start date (YYYY-MM-DD)"))
    start_time = models.TimeField(null=True, blank=True, verbose_name=_("Start time (format)"))
    end_time = models.TimeField(null=True, blank=True, verbose_name=_("End time (format)"))
    duration = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Duration (hours)"))
    identifier_string = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Identifier String"))

    def __str__(self):
        return self.identifier_string

    def get_absolute_url(self):
        return reverse("vault:outing_detail", kwargs={"pk": self.id})

class Observation(models.Model):
    outing = models.ForeignKey(Outing, on_delete=models.DO_NOTHING, related_name="sightings", verbose_name=_("Outing"))
    instrument = models.ForeignKey(Instrument, on_delete=models.DO_NOTHING, related_name="sightings", verbose_name=_("Instrument"))
    datetime = models.DateTimeField(null=True, blank=True, help_text="Format YYYY-MM-DD 00:00:00", verbose_name=_("Date and Time"))
    longitude = models.FloatField(null=True, blank=True, verbose_name=_("Longitude"))
    latitude = models.FloatField(null=True, blank=True, verbose_name=_("Latitude"))
    observer = models.ForeignKey(Person, on_delete=models.DO_NOTHING, related_name="sightings", verbose_name=_("Observer"), null=True, blank=True)
    metadata = models.ManyToManyField(MetadataField, through="ObservationMetadatum")
    opportunistic = models.BooleanField(default=False)

    def __str__(self):
        return self.outing.identifier_string

    def get_absolute_url(self):
        return reverse("vault:observation_detail", kwargs={"pk": self.id})

class ObservationMetadatum(models.Model):
    observation = models.ForeignKey(Observation, on_delete=models.DO_NOTHING, related_name="observation_metadata", verbose_name=_("Observation"))
    metadata_field = models.ForeignKey(MetadataField, on_delete=models.CASCADE, related_name="observation_metadata", verbose_name=_("Metadata field"))
    value = models.CharField(max_length=1000)


class Certainty(models.Model):
    code = models.IntegerField(blank=True, null=True, verbose_name=_("code"))
    english_certainty_description = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("description"))
    french_certainty_description = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("description"))


class Sex(models.Model):
    name = models.CharField(max_length=255)
    nom = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):

            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


class LifeStage(models.Model):
    name = models.CharField(max_length=255)
    nom = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):

            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


class HealthStatus(models.Model):
    name = models.CharField(max_length=255)
    nom = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):

            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]

class IndividualIdentification(models.Model):
    id_number = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):

            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]

class ObservationSighting(models.Model):
    observation = models.ForeignKey(Observation, on_delete=models.DO_NOTHING, related_name="observation_sightings", verbose_name=_("observation"))
    species = models.ForeignKey(Species, on_delete=models.DO_NOTHING, related_name="observation_sightings", null=True, blank=True)
    certainty = models.ForeignKey(Certainty, on_delete=models.DO_NOTHING, related_name="observation_sightings", null=True, blank=True)
    sex = models.ForeignKey(Sex, on_delete=models.DO_NOTHING, related_name="observation_sightings", null=True, blank=True)
    life_stage = models.ForeignKey(LifeStage, on_delete=models.DO_NOTHING, related_name="observation_sightings", null=True, blank=True)
    health_status = models.ForeignKey(HealthStatus, on_delete=models.DO_NOTHING, related_name="observation_sightings",
                                      null=True, blank=True)
    verified = models.BooleanField(default=False, verbose_name=_("verified"))
    known_individual = models.ForeignKey(IndividualIdentification, on_delete=models.DO_NOTHING, related_name="individual", verbose_name=_("known individual"))


class OriginalMediafile(models.Model):
    file_path = models.CharField(max_length=1000, blank=True, null=True)
    filename = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("filename"))
    observation = models.ForeignKey(Observation, on_delete=models.DO_NOTHING, related_name="original_mediafiles", verbose_name=_("observation"))
    metadata = models.ManyToManyField(MetadataField, through="OriginalMediafileMetadatum")


class OriginalMediafileMetadatum(models.Model):
    original_mediafile = models.ForeignKey(OriginalMediafile, on_delete=models.DO_NOTHING, related_name="original_mediafile_metadata",
                                           verbose_name=_("original media file"))
    metadata_field = models.ForeignKey(MetadataField, on_delete=models.CASCADE, related_name="original_mediafile_metadata")
    value = models.CharField(max_length=1000)


class FieldName(models.Model):
    field_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("name"))
    used_for = models.ManyToManyField(Instrument, verbose_name=_("used for"), blank=True)


class MediafileSighting(models.Model):
    original_mediafile = models.ForeignKey(OriginalMediafile, on_delete=models.DO_NOTHING, related_name="mediafile_sightings",
                                           verbose_name=_("original media file"))
    species = models.ForeignKey(Species, on_delete=models.DO_NOTHING, related_name="mediafile_sightings", null=True, blank=True)
    certainty = models.ForeignKey(Certainty, on_delete=models.DO_NOTHING, related_name="mediafile_sightings", null=True, blank=True)
    sex = models.ForeignKey(Sex, on_delete=models.DO_NOTHING, related_name="mediafile_sightings", null=True, blank=True)
    life_stage = models.ForeignKey(LifeStage, on_delete=models.DO_NOTHING, related_name="mediafile_sightings", null=True, blank=True)
    health_status = models.ForeignKey(HealthStatus, on_delete=models.DO_NOTHING, related_name="mediafile_sightings",
                                      null=True, blank=True)
    verified = models.BooleanField(default=False, verbose_name=_("verified"))
   # known_individual = models.ForeignKey(IndividualIdentification, on_delete=models.DO_NOTHING, related_name="individual", verbose_name=_("known individual"))


class ProcessedMediafile(models.Model):
    file_path = models.CharField(max_length=1000, blank=True, null=True)
    filename = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("filename"))
    original_mediafile = models.ForeignKey(OriginalMediafile, on_delete=models.DO_NOTHING, related_name="processed_mediafiles",
                                           verbose_name=_("original mediafile"))
    species = models.ManyToManyField(Species, verbose_name=_("species"), blank=True)
    verified = models.BooleanField(default=False, verbose_name=_("verified"))
    analyst = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    date_analysed = models.DateTimeField()
    date_created = models.DateTimeField()
