from django import forms
from django.core import validators
from . import models


class ResourceCreateForm(forms.ModelForm):
    add_custodian = forms.BooleanField(required=False, label="Add yourself as custodian")
    add_point_of_contact = forms.BooleanField(required=False, label="Add Regional Data Manager as a Point of Contact")
    class Meta:
        model = models.Resource
        exclude = [
            'file_identifier',
            'uuid',
            'date_verified',
            'date_last_modified',
            'fgp_publication_date',
            'citations',
            'keywords',
            'people',
        ]
        widgets = {
            'last_modified_by':forms.HiddenInput(),
        }


class ResourceForm(forms.ModelForm):
    class Meta:
        model = models.Resource
        exclude = [
            'file_identifier',
            'uuid',
            'date_verified',
            'date_last_modified',
            'fgp_publication_date',
            'citations',
            'keywords',
            'people',
        ]
        widgets = {
            'last_modified_by':forms.HiddenInput(),
        }

class ResourcePersonForm(forms.ModelForm):
    class Meta:
        model = models.ResourcePerson
        fields = "__all__"
        labels={
            'notes':"Notes (optional)",
            'longitude_w':"Longitude",
        }
        widgets = {
            'resource':forms.HiddenInput(),
            'person':forms.HiddenInput(),
            'notes':forms.Textarea(attrs={'rows':"5"}),
            # 'last_modified_by':forms.HiddenInput(),
        }



class PersonCreateForm(forms.Form):

    LANGUAGE_CHOICES = ((None,"---"),) + models.LANGUAGE_CHOICES

    ORGANIZATION_CHOICES = ((None,"---"),)
    for org in models.Organization.objects.all():
        ORGANIZATION_CHOICES = ORGANIZATION_CHOICES.__add__(((org.id,org.name_eng),))

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField(required=False)
    position_eng = forms.CharField(label="Position title (English)",required=False)
    position_fre = forms.CharField(label="Position title (French)",required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"000-000-0000 ext.000"}),required=False)
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES,required=False)
    organization = forms.ChoiceField(choices=ORGANIZATION_CHOICES,required=False)


class KeywordForm(forms.ModelForm):
    class Meta:
        model = models.Keyword
        exclude = [
            'concept_scheme',
            'xml_block',
            'is_taxonomic',
        ]


class CitationForm(forms.ModelForm):
    class Meta:
        model = models.Citation
        fields = ("__all__")
        # exclude = [
        #     'concept_scheme',
        #     'xml_block',
        #     'is_taxonomic',
        # ]


class ResourceCertificationForm(forms.ModelForm):
    class Meta:
        model = models.ResourceCertification
        fields = "__all__"
        labels={
            'notes':"Certification Notes",
        }
        widgets = {
            'certifying_user': forms.HiddenInput(),
            'resource': forms.HiddenInput(),
            'certification_date': forms.HiddenInput(),
            'notes': forms.Textarea(attrs={"rows":2}),
        }