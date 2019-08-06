from _ast import mod

from bokeh.core.property.dataspec import field
from django import forms
from whalesdb import models
from django.utils.translation import gettext_lazy as _
from django.forms.models import inlineformset_factory


def get_short_labels(for_model):

    # You can override the longer more descriptive labels from get_labels()
    # here. If not overriden the else clause will just call get_labels()

    if for_model is models.EqrRecorderProperties:
        labels = {
            'emm': _("Make & Model"),
            'eqc_max_channels': _("Max Channels"),
            'eqc_max_sample_rate': _("Max Sample Rate")
        }
    elif for_model is models.EqhHydrophoneProperties:
        labels = {
            'emm': _("Make & Model"),
            'eqh_range_min': _("Bottom frequency"),
            'eqh_range_max': _("Top frequency"),
        }
    elif for_model is models.EcpChannelProperties:
        labels = {
            'ecp_channel_no': _("Channel number"),
            'eqa_adc_bits': _("ADC Bits"),
            'ecp_voltage_range': _("Voltage Range"),
            'ecp_gain': _("Gain in dB."),
        }
    elif for_model is models.EprEquipmentParameters:
        labels = {
            'prm': _("Equipment Parameters"),
        }
    else:
        labels = get_labels(for_model)

    return labels


def get_labels(for_model):
    labels = {}
    if for_model is models.DepDeployments:
        labels = {
            'dep_name': _('Deployment Name'),
            'stn': _('Station'),
            'prj': _('Project'),
            'mor': _('Mooring Setup'),
        }
    elif for_model is models.MorMooringSetups:
        labels = {
            'mor_name': _('Mooring Setup Name'),
            'mor_max_depth': _('Max Depth'),
            'mor_num_hydrophones': _('Number of Hydrophones'),
            'mor_link_setup_image': _('Setup Image Location'),
            'mor_additional_equipment': _('Additional Equipment'),
            'mor_general_moor_description': _('General Description'),
            'more_notes': _('Notes'),
        }
    elif for_model is models.PrjProjects:
        labels = {
            'prj_name': _('Project Name'),
            'prj_descrption': _('Project Description'),
            'prj_url': _('Project URL'),
        }
    elif for_model is models.StnStations:
        labels = {
            'stn_name': _('Station Name'),
            'stn_planned_lat': _('Planned Latitude'),
            'stn_planned_lon': _('Planned Longitude'),
            'stn_planned_depth': _('Planned Depth'),
            'stn_notes': _('Station Notes'),
        }
    elif for_model is models.SteStationEvents:
        labels = {
            'dep': _('Deployment'),
            'set_type': _('Event Type'),
            'ste_date': _('Event Date'),
            'crs': _('Cruise'),
            'ste_lat_ship': _('Latitude, by ship instruments'),
            'ste_lon_ship': _('Longitude, by ship instruments'),
            'ste_depth_ship': _('Depth, by ship instruments'),
            'ste_lat_mcal': _('Latitude'),
            'ste_lon_mcal': _('Longitude'),
            'ste_depth_mcal': _('Depth'),
            'ste_team': _('Team'),
            'ste_instrument_cond': _('Instrument Conditions'),
            'ste_weather_cond': _('Weather Conditions'),
            'ste_logs': _('Event Log Location'),
            'ste_notes': _('Event Notes'),
        }
    elif for_model is models.CrsCruises:
        labels = {
            'crs_name': _('Cruise Name'),
            'crs_pi_name': _('Principal Investigator Name'),
            'crs_institute_name': _('Institute Name'),
            'crs_geographic_location': _('Geographic Location'),
            'crs_start_date': _('Start Date'),
            'crs_end_date': _('End Date'),
            'crs_notes': _('Cruise Notes'),
        }
    elif for_model is models.RecRecordingEvents:
        labels = {
            'tea_id_setup_by': _("Team member who programmed the recording setup"),
            'rec_date_of_system_chk': _("Recording date of the system check (Time in UTC)"),
            'tea_id_checked_by': _("Team member who prefored the System Check"),
            'rec_date_first_recording': _("Date of first recording when the equipment is turned on for deployment."),
            'rec_date_last_recording': _("Date of last recording"),
            'rec_total_memory_used': _("Total memory used for number of recorded files"),
            'rec_hf_mem': _("High Frequency Memory usage in Gigabytes (GB)"),
            'rec_lf_mem': _("Low Frequency Memory usage in Gigabytes (GB)"),
            'rec_date_data_download': _("Date the data has been downloaded from equipment"),
            'rec_data_store_url': _("URL of the location the data storage"),
            'tea_id_downloaded_by': _("Team member who backed up the data"),
            'rec_date_data_backed_up': _("Date data was backed up"),
            'rec_data_backup_url': _("URL of the data backup location"),
            'tea_id_backed_up_by': _("Team member who backed up the data"),
            'rec_channel_count': _("The number of channels used to record data, one recording per channel"),
            'rec_notes': _("Comments on the recording and data"),
            'rtt': _("Time zone data files use. Should be UTC, but occasionally for legacy data  will be in some "
                     "local format."),
            'rec_first_in_water': _("First in water recording"),
            'rec_last_in_water': _("Last in water recording"),
        }
    elif for_model is models.RscRecordingSchedules:
        labels = {
            'rec': _("Recording Event this recording schedule is associated with"),
            'rsc_name': _("A human readable name for this duty cycle if it is to be used as a preset configuration"),
            'rsc_period': _("Unit of time before the recording schedul repeats (seconds)"),
        }
    elif for_model is models.RstRecordingStage:
        labels = {
            'rst_channel_no': _("Channel Number this stage is being recorded on"),
            'rsc': _("The recording schedule this stage belongs to"),
            'rst_active': _("(A)ctive or (S)leep"),
            'rst_duration': _("The number of seconds this stage is active fore"),
            'rst_rate': _("Sampling rate in Hertz (Hz)"),
            'rst_gain': _("Decibles (dB)"),
        }
    elif for_model is models.TeaTeamMembers:
        labels = {
            'tea_last_name': _("Last Name of the team member"),
            'tea_first_name': _("First Name of the team Member"),
        }
    elif for_model is models.SetStationEventCode:
        labels = {
            'set_name': _('Station Event Code Name'),
            'set_description': _('Station Event Code Description'),
        }
    elif for_model is models.EmmMakeModel:
        labels = {
            'eqt': _("Equipment category"),
            'emm_make': _("Equipment make"),
            'emm_model': _("Equipment model"),
            'emm_depth_rating': _("The depth in metres this piece of equipment is rated for"),
            'emm_description': _("Short description of the piece of equipment"),
        }
    elif for_model is models.EqhHydrophoneProperties:
        labels = {
            'eqh_range_min': _("Bottom frequency in the functional flat range of the hydrophone in Hz (+-3 dB unless "
                               "stated in notes)"),
            'eqh_range_max': _("Top frequency in the functional flat range of the hydrophone in Hz (+-3 dB unless "
                               "stated in notes)"),
        }
    elif for_model is models.EqrRecorderProperties:
        labels = {
            'eqc_max_channels': _("Maximum number of channels a piece of equipment can handle."),
            'eqc_max_sample_rate': _("How fast data can be recorded in KHz"),
        }
    elif for_model is models.EcpChannelProperties:
        labels = {
            'ecp_channel_no': _("Channel number"),
            'eqa_adc_bits': _("ADC Bits represented in this channel"),
            'ecp_voltage_range': _("Voltage Range"),
            'ecp_gain': _("How much a channel is amplified in dB."),
        }
    elif for_model is models.EprEquipmentParameters:
        labels = {
            'prm': _("The parameter type attached to a piece of equipment"),
        }

    return labels


class DeploymentForm(forms.ModelForm):

    class Meta:
        model = models.DepDeployments
        labels = get_labels(model)
        fields = labels.keys()


class MooringForm(forms.ModelForm):

    class Meta:
        model = models.MorMooringSetups
        labels = get_labels(model)
        fields = labels.keys()
        widgets = {
            'mor_additional_equipment': forms.Textarea(attrs={"rows": 2}),
            'mor_general_moor_description': forms.Textarea(attrs={"rows": 2}),
            'more_notes': forms.Textarea(attrs={"rows": 2}),
        }


class ProjectForm(forms.ModelForm):

    class Meta:
        model = models.PrjProjects
        labels = get_labels(model)
        fields = labels.keys()
        widgets = {
            'prj_descrption': forms.Textarea(attrs={"rows": 2}),
        }


class StationForm(forms.ModelForm):

    class Meta:
        model = models.StnStations
        labels = get_labels(model)
        fields = labels.keys()
        widgets = {
            'stn_notes': forms.Textarea(attrs={"rows": 2}),
        }


class CruiseForm(forms.ModelForm):

    class Meta:
        model = models.CrsCruises
        labels = get_labels(model)
        fields = labels.keys()
        widgets = {
            'crs_notes': forms.Textarea(attrs={"rows": 2}),
        }


class CreateStationEventForm(forms.ModelForm):

    class Meta:
        model = models.SteStationEvents
        labels = get_labels(model)
        fields = labels.keys()
        widgets = {
            'ste_instrument_cond': forms.Textarea(attrs={"rows": 2}),
            'ste_weather_cond': forms.Textarea(attrs={"rows": 2}),
            'ste_logs': forms.Textarea(attrs={"rows": 2}),
            'ste_notes': forms.Textarea(attrs={"rows": 2}),
        }


class CreateRecordEventForm(forms.ModelForm):

    class Meta:
        model = models.RecRecordingEvents
        labels = get_labels(model)
        fields = labels.keys()


class CreateRecordScheduleForm(forms.ModelForm):

    class Meta:
        model = models.RscRecordingSchedules
        labels = get_labels(model)
        fields = labels.keys()


class CreateRecordStageForm(forms.ModelForm):

    class Meta:
        model = models.RstRecordingStage
        labels = get_labels(model)
        fields = labels.keys()


class CreateTeamForm(forms.ModelForm):

    class Meta:
        model = models.TeaTeamMembers
        labels = get_labels(model)
        fields = labels.keys()


class CreateStationEventCodeForm(forms.ModelForm):

    class Meta:
        model = models.SetStationEventCode
        labels = get_labels(model)
        fields = labels.keys()
        widgets = {
            'set_description': forms.Textarea(attrs={"rows": 2}),
        }


class EmmMakeModelForm(forms.ModelForm):

    class Meta:
        model = models.EmmMakeModel
        labels = get_labels(model)
        fields = labels.keys()


class EprEquipmentParametersForm(forms.ModelForm):

    class Meta:
        model = models.EprEquipmentParameters
        labels = get_labels(model)
        fields = labels.keys()


class EcpChannelPropertiesForm(forms.ModelForm):

    def get_initial_for_field(self, field, field_name):
        if field_name is 'ecp_channel_no':
            return 1

        return super().get_initial_for_field(field, field_name)

    class Meta:
        model = models.EcpChannelProperties
        labels = get_labels(model)
        fields = labels.keys()

class EqhHydrophonePropertiesForm(forms.ModelForm):

    eqt = forms.ChoiceField(label=_("Equipment category"))
    emm_make = forms.CharField(max_length=50, label=_("Equipment make"))
    emm_model = forms.CharField(max_length=50, label=_("Equipment model"))
    emm_depth_rating = forms.IntegerField(label=_("The depth in metres this piece of equipment is rated for"))
    emm_description = forms.CharField(max_length=500, label=_("Short description of the piece of equipment"))

    class Meta:
        model = models.EqhHydrophoneProperties

        p_lbls = get_labels(models.EmmMakeModel)
        fields = list(p_lbls.keys())

        labels = get_labels(model)
        fields.extend(list(labels.keys()))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        eqt_choices = models.EqtEquipmentTypeCode.objects.all().values_list()
        self.fields['eqt'].choices = eqt_choices


class EqrRecorderPropertiesForm(forms.ModelForm):

    eqt = forms.ChoiceField(label=_("Equipment category"))
    emm_make = forms.CharField(max_length=50, label=_("Equipment make"))
    emm_model = forms.CharField(max_length=50, label=_("Equipment model"))
    emm_depth_rating = forms.IntegerField(label=_("The depth in metres this piece of equipment is rated for"))
    emm_description = forms.CharField(max_length=500, label=_("Short description of the piece of equipment"))

    class Meta:
        model = models.EqrRecorderProperties

        p_lbls = get_labels(models.EmmMakeModel)
        fields = list(p_lbls.keys())

        labels = get_labels(model)
        fields.extend(list(labels.keys()))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        eqt_choices = models.EqtEquipmentTypeCode.objects.all().values_list()
        self.fields['eqt'].choices = eqt_choices


class CodeEditForm(forms.ModelForm):

    value = forms.CharField(max_length=255, label="")

    class Meta:
        model = models.EqaAdcBitsCode
        fields = ['value']