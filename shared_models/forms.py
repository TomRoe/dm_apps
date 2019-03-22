from django import forms
from django.contrib.auth.models import User
from django.core import validators
from . import models


class SectionForm(forms.ModelForm):
    class Meta:
        model = models.Section
        exclude = [
            'date_last_modified',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),

        }

    def __init__(self, *args, **kwargs):
        USER_CHOICES = [(u.id, "{}, {}".format(u.last_name, u.first_name)) for u in
                        User.objects.all().order_by("last_name", "first_name")]
        USER_CHOICES.insert(0, tuple((None, "---")))

        super().__init__(*args, **kwargs)
        self.fields['head'].choices = USER_CHOICES


class DivisionForm(forms.ModelForm):
    class Meta:
        model = models.Division
        exclude = [
            'date_last_modified',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),

        }

class BranchForm(forms.ModelForm):
    class Meta:
        model = models.Branch
        exclude = [
            'date_last_modified',
        ]
        widgets = {
            'last_modified_by': forms.HiddenInput(),

        }